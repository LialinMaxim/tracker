from django.test import TestCase, override_settings
from django.db.utils import IntegrityError
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .models import CheckResults


class ExceptionViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        email = 'admin@gmail.com'
        password = 'great'

        self.auth = self.signup_and_login(email, password)

        email = 'admin2@gmail.com'
        password = 'great'

        self.auth2 = self.signup_and_login(email, password)

    @staticmethod
    def get_auth_header_by_token(token):
        return {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    def signup_and_login(self, email, password):
        response = self.client.post(reverse('accounts-signup'), {'email': email, 'password': password})
        self.assertEqual(response.status_code, 201)

        response = self.client.post(reverse('accounts-login'), {'email': email, 'password': password})
        self.assertEqual(response.status_code, 200)

        token = response.json()['token']
        self.assertTrue(bool(token))

        return self.get_auth_header_by_token(token)

    def test_empty_results(self):
        response = self.client.get(reverse('data-checkresults'), **self.auth2)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()), 0)

    def test_storage(self):
        data = {'data': {'flying': True}}

        response = self.client.post(reverse('data-checkresults'), data, 'json', **self.auth)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('data-checkresults'), **self.auth)
        result = response.json()
        print(result)
        self.assertEqual(len(result), 1)
        self.assertDictEqual(result[0]['data'], data['data'])

        self.assertTrue(bool(result[0]['user_id']))
        self.assertTrue(bool(result[0]['created_at']))

    def test_storage_order(self):
        expected_data = []

        for years in range(10):
            data = {'data': {'years': years}}
            expected_data.insert(0, data)

            response = self.client.post(reverse('data-checkresults'), data, 'json', **self.auth)
            self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('data-checkresults'), **self.auth)
        result = response.json()

        self.assertEqual(len(result), len(expected_data))

        for item, expected_item in zip(result, expected_data):
            self.assertDictEqual(item['data'], expected_item['data'])
