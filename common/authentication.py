import jwt
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class CustomTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate_credentials(self, token):
        try:
            decoded_token = jwt.decode(
                token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM, options={'verify_exp': True})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token is invalid.', 'invalid_token')

        username = decoded_token['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed('No such user.', 'user_not_found')
        else:
            return user, token
