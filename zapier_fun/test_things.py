import unittest

from zapier_fun.app import app


class ZapierFunTests(unittest.TestCase):

    def test_index_returns_302(self):
        request, response = app.test_client.get('/', allow_redirects=False)
        self.assertEqual(response.status, 302)
        self.assertEqual(response.headers['Location'], '/introduce')

    def test_introduce(self):
        request, response = app.test_client.get('/introduce')
        self.assertEqual(response.status, 200)

    def test_introduce_form_input(self):
        request, response = app.test_client.post('/introduce', data=dict(
            email="test@test", first_name="test", last_name="test"))
        self.assertEqual(response.status, 400)

    def test_introduce_form_redirect_on_success(self):
        request, response = app.test_client.post('/introduce', data=dict(
            email="test@test.com", first_name="test", last_name="test"),
                                                 allow_redirects=False)
        self.assertEqual(response.status, 302)
        self.assertEqual(response.headers['Location'], '/thanks')

    def test_api_introduce_invalid_input(self):

        payload = {
            "email": "test@test",
            "first_name": "x" * 51,
            "last_name": "x" * 51
        }

        request, response = app.test_client.post(
            '/api/v1/introduce', json=payload)

        self.assertEqual(response.status, 400)

        self.assertIsNotNone(response.json.get('errors'))

        for i in ["email", "first_name", "last_name"]:
            self.assertIsNotNone(response.json['errors'].get(i))


if __name__ == '__main__':
    unittest.main()
