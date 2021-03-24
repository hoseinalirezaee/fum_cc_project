from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class UserAlreadyExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('A user with this username already exists.')
    default_code = 'already_exists'
