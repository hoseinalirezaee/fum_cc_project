from common.services import auth_services
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Doctor(models.Model):
    id = models.CharField(_('User ID'), max_length=128, primary_key=True)
    username = models.CharField(_('Username'), max_length=128)
    first_name = models.CharField(_('First Name'), max_length=64)
    last_name = models.CharField(_('Last Name'), max_length=64)
    phone = models.CharField(_('Phone'), max_length=16, null=False, default='')
    men = models.CharField(_('Medical Education Number'), max_length=11, default='')
    address = models.TextField(_('Address'), max_length=8192, default='')
    city = models.CharField(_('City'), max_length=64, default='')
    expertise = models.CharField(_('Expertise'), max_length=64, default='')

    class Meta:
        ordering = ('last_name', 'first_name')


class AppointmentTime(models.Model):
    date = models.DateField(default=timezone.now)
    time_from = models.TimeField(default=timezone.now)
    time_to = models.TimeField(default=timezone.now)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                               related_name='appointment_times', related_query_name='appointment_times')

    class Meta:
        ordering = ('date', 'time_from', 'time_to')

    def reserve(self, user_id):
        return Reservation.objects.create(doctor=self.doctor, patient_id=user_id, appointment=self)


class Reservation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                               related_name='reservations', related_query_name='reservations')

    patient_id = models.CharField(_('User ID'), max_length=128, default='')

    appointment = models.ForeignKey(AppointmentTime, on_delete=models.PROTECT,
                                    related_name='reservations', related_query_name='reservations')


class Comment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                               related_name='comments', related_query_name='comments')
    patient_id = models.CharField(_('User ID'), max_length=128, default='')
    date_added = models.DateTimeField(default=timezone.now)
    text = models.TextField(max_length=4096)

    @staticmethod
    def create_comment(doc, patient_id, text):
        if auth_services.get_rule(patient_id) == auth_services.UserRule.PATIENT and text:
            comment = Comment.objects.create(doctor=doc, patient_id=patient_id, text=text)
            return comment
