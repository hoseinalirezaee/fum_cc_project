from unittest import mock

from django.test import TestCase

from users import models


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
