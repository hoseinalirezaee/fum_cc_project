from django.conf import settings
from rest_framework.authentication import BasicAuthentication


class AuthenticatedUser:
    @property
    def is_authenticated(self):
        return True


class UnAuthenticatedUser:
    @property
    def is_authenticated(self):
        return False


class CustomBasicAuthentication(BasicAuthentication):
    def authenticate_credentials(self, userid, password, request=None):
        if userid == settings.BASIC_AUTH_USERNAME and password == settings.BASIC_AUTH_PASSWORD:
            return (AuthenticatedUser(), None)
