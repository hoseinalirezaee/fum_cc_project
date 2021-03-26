from datetime import timedelta

import jwt
from api.models import User
from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed

from common.authentication import CustomTokenAuthentication


class TestAuthentication(TestCase):
    def test_custom_token_authentication(self):
        auth_class = CustomTokenAuthentication()
        now = timezone.now()

        payload = {'user_id': 'does_not_exist', 'exp': (now + timedelta(days=1)).timestamp()}
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        self.assertRaises(AuthenticationFailed, auth_class.authenticate_credentials, token)

        payload = {'user_id': 'hosein', 'exp': (now + timedelta(days=1)).timestamp()}
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        user = User.objects.create(username='hosein', first_name='Hosein', last_name='Alirezaee', id='hosein')
        auth_user = auth_class.authenticate_credentials(token)
        self.assertEqual(user.username, auth_user[0].username)
