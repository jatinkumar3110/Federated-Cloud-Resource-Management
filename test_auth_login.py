"""Authentication tests for demo login and invalid credential handling."""

import os
import unittest

import app as app_module


class LoginAuthTests(unittest.TestCase):
    def setUp(self):
        app_module.app.config['TESTING'] = True
        self.client = app_module.app.test_client()
        self.original_demo_flag = app_module.DEMO_LOGIN_ENABLED
        app_module.DEMO_LOGIN_ENABLED = True

    def tearDown(self):
        app_module.DEMO_LOGIN_ENABLED = self.original_demo_flag

    def test_quick_demo_credentials_login_success(self):
        response = self.client.post(
            '/login',
            data={'username': 'demo', 'password': 'demo'},
            follow_redirects=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.headers.get('Location', ''))

        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get('username'), 'demo')
            self.assertEqual(sess.get('role'), 'user')

    def test_invalid_credentials_rejected(self):
        response = self.client.post(
            '/login',
            data={'username': 'invalid', 'password': 'wrong'},
            follow_redirects=False,
        )

        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid credentials', response.data)

    def test_existing_admin_login_still_works(self):
        admin_password = os.getenv('ADMIN_PASSWORD', 'Admin@12345')
        response = self.client.post(
            '/login',
            data={'username': 'admin', 'password': admin_password},
            follow_redirects=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.headers.get('Location', ''))

        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get('username'), 'admin')
            self.assertEqual(sess.get('role'), 'admin')


if __name__ == '__main__':
    unittest.main()
