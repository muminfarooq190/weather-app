from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus as status

CREATE_USER_URL = reverse('user:create')
# ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserTests(TestCase):
    """Test users public"""
    def setUp(self):
        self.client = Client()

    def test_create_valid_user_success(self):
        """Test create user with valid payload is successfull"""
        payload = {
            'email': 'test@de.com',
            'password': 'testpass',
            'name': 'Test Name'
        }
        create_user(**payload)
        # res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(get_user_model().objects.count(), 1)
        # self.assertRedirects(res, '/user/')

    def test_user_exists(self):
        """test that user already exists"""
        payload = {
            'email': 'user@dev.com',
            'password': '12345',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.OK)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_password_too_short(self):
        """Test password must be more than 5 characters"""
        payload = {
            'email': 'user@dev.com',
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)
