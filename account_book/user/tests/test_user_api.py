from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
LOGOUT_URL = reverse('user:logout')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicAPITest(TestCase):
    '''public user api �׽�Ʈ'''

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        '''ȸ������ �׽�Ʈ'''
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        user = get_user_model().objects.get(email=payload['email'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_password_too_short_error(self):
        '''ª�� ��й�ȣ �Է� �� ���� '''
        payload = {
            'email': 'test@gmail.com',
            'password': 'pw',
            'name': 'test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        '''�α��� �� ��ū ����'''
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
        }

        get_user_model().objects.create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        '''�߸��� ���� �Է� �� ��ū �̻���'''
        payload1 = {
            'email': 'test@gmail.com',
            'password': 'testpass',
        }
        res = self.client.post(CREATE_USER_URL, payload1)

        payload2 = {
            'email': 'test@gmail.com',
            'password': 'wrong',
        }

        res = self.client.post(TOKEN_URL, payload2)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateAPITest(TestCase):
    '''�α��� ����� API �׽�Ʈ'''

    def setUp(self):
        user = {
            'email': 'test@gmail.com',
            'password': 'testpass',
        }
        self.user = create_user(**user)
        self.client = APIClient()

        res = self.client.post(TOKEN_URL, user)

        self.client.force_authenticate(
            user=self.user, token=self.user.auth_token)

    def test_logout_delete_token(self):
        '''�α׾ƿ� �� ��ū ����'''
        res = self.client.get(LOGOUT_URL)
        self.user.refresh_from_db()

        self.assertFalse(hasattr(self.user, 'auth_token'))
