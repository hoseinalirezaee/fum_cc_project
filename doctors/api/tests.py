from datetime import timedelta
from unittest import mock
from uuid import uuid1

import jwt
from common.services import auth_services
from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from api import models


def get_auth_header(user_id):
    data = {
        'user_id': user_id,
        'exp': (timezone.now() + timedelta(days=1)).timestamp()
    }
    token = jwt.encode(data, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    return 'Bearer %s' % token


class TestComment(TestCase):

    @mock.patch('common.services.auth_services.get_rule')
    def test_create_comment(self, mocked_get_rule):
        doc = models.Doctor.objects.create(id=uuid1(), username='username', first_name='Hosein', last_name='Alirezaee')
        user_id = '123'
        auth_header = get_auth_header(user_id)
        data = {
            'text': 'Test text.'
        }
        mocked_get_rule.return_value = auth_services.UserRule.PATIENT
        response = self.client.post('/doctors/%s/comments/' % doc.id, data=data, HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, 201)
        comment = models.Comment.objects.get(doctor=doc)
        self.assertEqual(comment.text, 'Test text.')


class TestDoctorsList(TestCase):
    def test_doctor_list(self):
        models.Doctor.objects.create(username='hosein', first_name='Hosein', last_name='Alirezaee')
        models.Doctor.objects.create(username='ali', first_name='Ali', last_name='Ghasemi')
        models.Doctor.objects.create(username='vahid', first_name='Vahid', last_name='Baghani')
        models.Doctor.objects.create(username='pouria', first_name='Pouria', last_name='Ghadiri')

        response = self.client.get('/doctors/list/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 4)
