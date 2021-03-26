from common.services import auth_services
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.exceptions import UserAlreadyExists


class User(models.Model):
    username = models.CharField(_('Username'), primary_key=True, max_length=128)
    id = models.CharField(_('User ID'), max_length=128, default='')
    first_name = models.CharField(_('First Name'), max_length=64)
    last_name = models.CharField(_('Last Name'), max_length=64)
    phone = models.CharField(_('Phone'), max_length=16, null=False, default='')
    favorite_doctors = ArrayField(base_field=models.CharField(max_length=128), default=list)

    def add_favorite_doctor(self, doc_id):
        if auth_services.get_rule(doc_id) == auth_services.UserRule.DOCTOR:
            if doc_id not in self.favorite_doctors:
                self.favorite_doctors.append(doc_id)
                self.save(update_fields=['favorite_doctors'])

    @staticmethod
    def create_user(username, first_name, last_name, password):
        qs = User.objects.filter(username=username)
        if not qs.exists():
            user_id = auth_services.create_user(username, password, auth_services.UserRule.PATIENT)
            if user_id:
                user = User.objects.create(username=username, first_name=first_name, last_name=last_name, id=user_id)
                return user

        raise UserAlreadyExists(detail='A user with username `%s` already exists.' % username)
