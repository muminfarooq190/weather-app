from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


class ModelTests(TestCase):
    def test_create_user_with_email_successfull(self):
        """Test create user with email"""
        email = "muminfarooq586@gmail.com"
        password = "testpass"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email(self):
        """Test to normalise email for a new user"""
        email = "test@dev.com"
        password = "testpass"
        user = get_user_model().objects.create_user(email, password)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test email for a new user"""
        email = None
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email, 'test123')

    def test_create_new_super_user(self):
        """Test creating a new super user"""
        email = "test123@dev.com"
        password = "testpass"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_user_str(self):
        """Test string representation of user"""
        email = "test@dev.com"
        password = "testpass"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, str(email))
