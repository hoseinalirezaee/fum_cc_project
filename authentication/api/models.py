from uuid import uuid1

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.enums import TextChoices
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, username, password, rule):
        user = self.model(username=username, rule=rule)
        user.set_password(password)
        user.save()
        return user

    def create_patient(self, username, password):
        return self._create_user(username, password, self.model.Rules.PATIENT)

    def create_doctor(self, username, password):
        return self._create_user(username, password, self.model.Rules.DOCTOR)


class User(AbstractBaseUser):

    class Rules(TextChoices):
        DOCTOR = 'DOCTOR'
        PATIENT = 'PATIENT'

    id = models.CharField(_('Unique ID'), max_length=128, default=uuid1, primary_key=True)
    username = models.CharField(_('Username'), max_length=64)
    rule = models.CharField(max_length=16, choices=Rules.choices)

    objects = UserManager()
