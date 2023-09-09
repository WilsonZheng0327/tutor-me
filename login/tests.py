from django.test import TestCase

from login.models import User

# Create your tests here.


class LoginModelTests(TestCase):
    def test_create_user_email(self):
        user = User(self, email='email@email.com', password='password',
                                        is_staff=True, is_superuser=False)
        self.assertEqual(user.email, 'email@email.com')

    def test_create_user_password(self):
        user = User(self, email='email@email.com', password='password',
                                        is_staff=True, is_superuser=False)
        self.assertEqual(user.password, 'password')

    def test_create_user_is_staff(self):
        user = User(self, email='email@email.com', password='password',
                                        is_staff=True, is_superuser=False)
        self.assertEqual(user.is_staff, True)

    def test_create_user_is_superuser(self):
        user = User(self, email='email@email.com', password='password',
                                        is_staff=True, is_superuser=False)
        self.assertEqual(user.is_superuser, False)

    def user_test_get_absolute_url(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.get_absolute_url(), '/users/1')
