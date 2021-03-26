from base64 import b64encode
from uuid import UUID

import jwt
from django.conf import settings
from django.test import TestCase

from api import models


class TestUserCreation(TestCase):
    def _test_user(self, create_func, username, password, rule):
        create_func(username, password)
        user = models.User.objects.get(username=username)
        self.assertEqual(user.rule, rule.value)
        self.assertTrue(user.check_password(password))
        uuid = UUID(user.id)
        self.assertEqual(uuid.version, 1)

    def test_create_patient(self):
        self._test_user(models.User.objects.create_patient, 'hosein', 'password', models.User.Rules.PATIENT)

    def test_create_doctor(self):
        self._test_user(models.User.objects.create_doctor, 'hosein', 'password', models.User.Rules.DOCTOR)


class TestGetToken(TestCase):
    def test_get_token(self):
        user = models.User.objects.create_patient(username='hosein', password='1')
        response = self.client.post('/authentication/get_token/', data={'username': 'hosein', 'password': 1})
        data = jwt.decode(response.json()['token'], algorithms=settings.JWT_ALGORITHM, key=settings.JWT_SECRET)
        self.assertEqual(data['user_id'], str(user.id))


class TestGetRule(TestCase):
    def test_get_rule(self):
        user = models.User.objects.create_patient(username='hosein', password='1')
        digest = '%s:%s' % (settings.BASIC_AUTH_USERNAME, settings.BASIC_AUTH_PASSWORD)
        digest = digest.encode('utf-8')
        digest = b64encode(digest).decode('utf-8')
        response = self.client.get('/internal/users/%s/rule/' % str(user.id), HTTP_AUTHORIZATION='BASIC %s' % digest)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['rule'], user.rule)
