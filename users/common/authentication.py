import jwt
from api.models import User
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class UnAuthenticatedUser:
    @property
    def is_authenticated(self):
        return False


class CustomTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate_credentials(self, token):
        try:
            decoded_token = jwt.decode(
                token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM, options={'verify_exp': True})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token is invalid.', 'invalid_token')

        user_id = decoded_token['user_id']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('No such user.', 'user_not_found')
        else:
            return user, token
