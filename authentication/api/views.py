import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework import exceptions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class GetTokenView(APIView):

    def perform_authentication(self, request):
        pass

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        try:
            user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            raise exceptions.NotFound('No user found with username `%s`' % username, 'does_not_exist')
        else:
            if user.check_password(serializer.validated_data['password']):
                payload = {
                    'user_id': user.id,
                    'exp': (timezone.now() + settings.JWT_LIFETIME).timestamp()
                }
                token = jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)
                return Response({'token': token}, status=200)

            else:
                return Response({'status': 'incorrect_password'}, status=status.HTTP_403_FORBIDDEN)


get_token_view = GetTokenView.as_view()

__all__ = ['get_token_view']
