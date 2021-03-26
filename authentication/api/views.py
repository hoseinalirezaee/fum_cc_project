import jwt
from common.authentication import CustomBasicAuthentication
from django.conf import settings
from django.utils import timezone
from rest_framework import (exceptions, permissions, serializers, status,
                            validators)
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


class GetUserRuleView(APIView):
    authentication_classes = [CustomBasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            raise exceptions.NotFound('No user found with user_id `%s`' % user_id, 'does_not_exist')
        else:
            return Response({'status': 'ok', 'rule': user.rule}, status=status.HTTP_200_OK)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'password', 'rule']
        extra_kwargs = {
            'username': {
                'validators': [validators.UniqueValidator(queryset=model.objects.all())]
            }
        }

    def create(self, validated_data):
        return models.User.objects.create_user(validated_data['username'],
                                               validated_data['password'],
                                               validated_data['rule'])


class RegisterUserView(APIView):
    authentication_classes = [CustomBasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'status': 'ok', 'user_id': user.id}, status=status.HTTP_201_CREATED)


get_token_view = GetTokenView.as_view()
get_rule_view = GetUserRuleView.as_view()
register_view = RegisterUserView.as_view()

__all__ = ['get_token_view', 'get_rule_view', 'register_view']
