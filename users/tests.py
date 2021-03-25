from datetime import timedelta
from unittest import mock

import jwt
from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from users import models


def get_token(user):
    data = {
        'username': user.username,
        'exp': (timezone.now() + timedelta(days=1)).timestamp()
    }
    token = jwt.encode(data, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    return token


class UserCreateTest(TestCase):

    @mock.patch('common.services.auth_services.create_user')
    def test_create_user(self, mocked_create_user):
        data = {
            'username': 'hosein',
            'password': '123',
            'first_name': 'Hosein',
            'last_name': 'Alirezaee'
        }
        mocked_create_user.return_value = True

        response = self.client.post('/users/create/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertNotIn('password', response.json())
        self.assertTrue(models.User.objects.filter(username='hosein').exists())

        response = self.client.post('/users/create/', data=data)
        self.assertEqual(response.status_code, 400)

    @mock.patch('common.services.auth_services.create_user')
    def test_create_user_failed(self, mocked_create_user):
        data = {
            'username': 'hosein',
            'password': '123',
            'first_name': 'Hosein',
            'last_name': 'Alirezaee'
        }
        mocked_create_user.return_value = False

        response = self.client.post('/users/create/', data=data)
        self.assertEqual(response.status_code, 400)


class UserAddFavoriteDoc(TestCase):

    @mock.patch('common.services.doctors_services.is_doctor')
    def test_add_favorite_doc(self, mocked_is_doctor):
        user = models.User.objects.create(first_name='Hosein', last_name='Alirezaee', username='hosein')
        token = get_token(user)

        mocked_is_doctor.return_value = True
        self.client.post('/users/add_favorite_doc/', data={'doc_id': 100}, HTTP_AUTHORIZATION='Bearer %s' % token)
        user.refresh_from_db()
        self.assertEqual(len(user.favorite_doctors), 1)
        self.assertIn('100', user.favorite_doctors)


class TestUserUpdate(TestCase):

    def test_user_update(self):
        user = models.User.objects.create(username='hosein', first_name='Hossein', last_name='Alirezaee')
        token = get_token(user)

        self.assertEqual(user.first_name, 'Hossein')
        self.assertEqual(user.phone, '')

        new_data = {'first_name': 'Hosein', 'phone': '09151234567'}
        self.client.post('/users/update/', data=new_data, HTTP_AUTHORIZATION='Bearer %s' % token)

        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Hosein')
        self.assertEqual(user.phone, '09151234567')
