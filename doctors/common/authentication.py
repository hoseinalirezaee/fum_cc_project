import jwt
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from common.services import auth_services


class AuthenticatedUser:
    def __init__(self, user_id) -> None:
        self.user_id = user_id

    @property
    def is_authenticated(self):
        return True


class CustomTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate_credentials(self, token):
        try:
            decoded_token = jwt.decode(
                token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM, options={'verify_exp': True})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token is invalid.', 'invalid_token')

        user_id = decoded_token['user_id']
        if auth_services.get_rule(user_id) == auth_services.UserRule.PATIENT:
            return AuthenticatedUser(user_id), token

        raise AuthenticationFailed('No such user.', 'user_not_found')
