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
        response = self.client.post('/doctors/%s/comments/' % doc.id, data=data, HTTP_AUTHORIZATION=auth_header,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        comment = models.Comment.objects.get(doctor=doc)
        self.assertEqual(comment.text, 'Test text.')


class TestDoctorsList(TestCase):
    def setUp(self) -> None:
        ids = [str(uuid1()) for _ in range(4)]
        models.Doctor.objects.create(id=ids[0], username='hosein', first_name='Hosein', last_name='Alirezaee')
        models.Doctor.objects.create(id=ids[1], username='ali', first_name='Ali', last_name='Ghasemi')
        models.Doctor.objects.create(id=ids[2], username='vahid', first_name='Vahid', last_name='Baghani')
        models.Doctor.objects.create(id=ids[3], username='pouria', first_name='Pouria', last_name='Ghadiri')

        self.ids = ids

    def test_doctor_list(self):
        response = self.client.get('/doctors/list/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 4)

    def test_internal_doctor_list(self):
        ids = self.ids[:2]
        response = self.client.post('/internal/doctors/list/', data={'doc_ids': ids}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 2)
        for doc in response.json()['results']:
            self.assertIn(doc['id'], ids)


class TestAppoinmentList(TestCase):

    def test_appoinment_list(self):
        doc = models.Doctor.objects.create(id=uuid1(), username='hosein', first_name='Hosein', last_name='Alirezaee')
        for _ in range(5):
            models.AppointmentTime.objects.create(doctor=doc)

        response = self.client.get('/doctors/%s/appointments/' % str(doc.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 5)


class TestReservetion(TestCase):
    @mock.patch('common.services.auth_services.get_rule')
    def test_reservation(self, mocked_get_rule):
        doc = models.Doctor.objects.create(id=uuid1(), username='hosein', first_name='Hosein', last_name='Alirezaee')
        appointment = models.AppointmentTime.objects.create(doctor=doc)

        mocked_get_rule.return_value = auth_services.UserRule.PATIENT
        response = self.client.post('/doctors/appointments/%s/reserve/' % appointment.id,
                                    HTTP_AUTHORIZATION=get_auth_header('100'), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(models.Reservation.objects.filter(id=response.json()['reservation_id']).exists())
