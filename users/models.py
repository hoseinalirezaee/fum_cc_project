from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    username = models.CharField(_('Username'), primary_key=True, max_length=128)
    first_name = models.CharField(_('First Name'), max_length=64)
    last_name = models.CharField(_('Last Name'), max_length=64)
    favorite_doctors = ArrayField(base_field=models.CharField(max_length=128), default=list)


class ReservedTimes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reserved_times',
                             related_query_name='reserved_times')
    doctor_id = models.IntegerField()
    date = models.DateTimeField()
