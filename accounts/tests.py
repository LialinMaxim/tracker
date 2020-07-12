from django.test import TestCase, override_settings
from django.db.utils import IntegrityError
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .models import User


class AccountsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

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

    def test_signup(self):
        response = self.client.post(reverse('accounts-signup'), {'email': 'admin@gmail.com', 'password': 'great'})
        self.assertEqual(response.status_code, 201)

    def test_double_signup(self):
        response = self.client.post(reverse('accounts-signup'), {
            'email': 'admin2@gmail.com',
            'password': 'great'
        })
        self.assertEqual(response.status_code, 201)

        with self.assertRaises(IntegrityError):
            self.client.post(reverse('accounts-signup'), {'email': 'admin2@gmail.com', 'password': 'great'})

    def test_login(self):
        email = 'admin3@gmail.com'
        password = 'great'

        self.signup_and_login(email, password)

    def test_isloggedin(self):
        email = 'admin4@gmail.com'
        password = 'great'

        auth_header =  self.signup_and_login(email, password)

        response = self.client.get(reverse('accounts-isloggedin'), **auth_header)
        self.assertEqual(response.status_code, 200)

    def test_ispaid(self):
        email = 'admin5@gmail.com'
        password = 'great'

        auth_header = self.signup_and_login(email, password)

        response = self.client.get(reverse('accounts-ispaiduser'), **auth_header)
        self.assertEqual(response.status_code, 403)

        User.objects.filter(email=email).update(payment_info={'card': 'XXXX-XXXX-XXXX-XXXX'})

        response = self.client.get(reverse('accounts-ispaiduser'), **auth_header)
        self.assertEqual(response.status_code, 200)
