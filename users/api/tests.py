from datetime import timedelta
from unittest import mock

import jwt
from common.services import auth_services
from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from api import models


def get_token(user):
    data = {
        'user_id': user.id,
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
        mocked_create_user.return_value = '123456'

        response = self.client.post('/users/create/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertNotIn('password', response.json())
        user = models.User.objects.get(username='hosein')
        self.assertEqual(user.id, '123456')

        response = self.client.post('/users/create/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    @mock.patch('common.services.auth_services.create_user')
    def test_create_user_failed(self, mocked_create_user):
        data = {
            'username': 'hosein',
            'password': '123',
            'first_name': 'Hosein',
            'last_name': 'Alirezaee'
        }
        mocked_create_user.return_value = None

        response = self.client.post('/users/create/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)


class TestUserFavoriteDoc(TestCase):

    @mock.patch('common.services.auth_services.get_rule')
    def test_add_favorite_doc(self, mocked_is_doctor):
        user = models.User.objects.create(first_name='Hosein', last_name='Alirezaee', username='hosein', id='hosein')
        token = get_token(user)

        mocked_is_doctor.return_value = auth_services.UserRule.DOCTOR
        self.client.post('/users/favorite_doc/add/', data={'doc_id': '100'}, HTTP_AUTHORIZATION='Bearer %s' % token,
                         content_type='application/json')
        user.refresh_from_db()
        self.assertEqual(len(user.favorite_doctors), 1)
        self.assertIn('100', user.favorite_doctors)

    def test_remove_doc(self):
        user = models.User.objects.create(first_name='Hosein', last_name='Alirezaee', username='hosein', id='hosein',
                                          favorite_doctors=['1', '2'])
        token = get_token(user)
        resposne = self.client.delete('/users/favorite_doc/remove/', data={'doc_id': '3'},
                                      content_type='application/json',
                                      HTTP_AUTHORIZATION='Bearer %s' % token)
        self.assertEqual(resposne.status_code, 200)

        self.client.delete('/users/favorite_doc/remove/', data={'doc_id': '1'}, content_type='application/json',
                           HTTP_AUTHORIZATION='Bearer %s' % token)
        user.refresh_from_db()
        self.assertEqual(len(user.favorite_doctors), 1)
        self.assertIn('2', user.favorite_doctors)

    @mock.patch('common.services.doc_services.get_docs_info')
    def test_list_favorite_doctors(self, mocked_get_docs_info):
        user = models.User.objects.create(first_name='Hosein', last_name='Alirezaee', username='hosein', id='hosein',
                                          favorite_doctors=['1', '2'])
        token = get_token(user)
        d = [{'name': '1'}, {'name': '2'}]
        mocked_get_docs_info.return_value = d
        response = self.client.get('/users/favorite_doc/list/', HTTP_AUTHORIZATION='Bearer %s' % token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), d)
        mocked_get_docs_info.assert_called_with(['1', '2'])


class TestUserUpdate(TestCase):

    def test_user_update(self):
        user = models.User.objects.create(username='hosein', first_name='Hossein', last_name='Alirezaee')
        token = get_token(user)

        self.assertEqual(user.first_name, 'Hossein')
        self.assertEqual(user.phone, '')

        new_data = {'first_name': 'Hosein', 'phone': '09151234567'}
        self.client.post('/users/update/', data=new_data, HTTP_AUTHORIZATION='Bearer %s' % token,
                         content_type='application/json')

        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Hosein')
        self.assertEqual(user.phone, '09151234567')
