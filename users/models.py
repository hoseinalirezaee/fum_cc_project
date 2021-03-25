from common.services import auth_services, doctors_services
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.exceptions import UserAlreadyExists


class User(models.Model):
    username = models.CharField(_('Username'), primary_key=True, max_length=128)
    first_name = models.CharField(_('First Name'), max_length=64)
    last_name = models.CharField(_('Last Name'), max_length=64)
    favorite_doctors = ArrayField(base_field=models.CharField(max_length=128), default=list)

    def add_favorite_doctor(self, doc_id):
        if doctors_services.is_doctor(doc_id):
            if doc_id not in self.favorite_doctors:
                self.favorite_doctors.append(doc_id)
                self.save(update_fields=['favorite_doctors'])

    @staticmethod
    def create_user(username, first_name, last_name, password):
        qs = User.objects.filter(username=username)
        if not qs.exists() and auth_services.create_user(username, password, 'normal'):
            user = User.objects.create(username=username, first_name=first_name, last_name=last_name)
            return user

        raise UserAlreadyExists(detail='A user with username `%s` already exists.' % username)


class ReservedTimes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reserved_times',
                             related_query_name='reserved_times')
    doctor_id = models.IntegerField()
    date = models.DateTimeField()
