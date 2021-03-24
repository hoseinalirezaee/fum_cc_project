from rest_framework import serializers, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users import models


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)
    first_name = serializers.CharField(max_length=64)
    last_name = serializers.CharField(max_length=64)

    def create(self, validated_data):
        user = models.User.create_user(**validated_data)
        return user


class UserViewSet(CreateModelMixin, GenericViewSet):

    def get_serializer_class(self):
        if self.action == 'create_user':
            return UserCreateSerializer
        return super().get_serializer_class()

    def perform_authentication(self, request):
        if self.action == 'create_user':
            return

        super().perform_authentication(request)

    def create_user(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        del serializer.validated_data['password']
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


create_user_view = UserViewSet.as_view(actions={'post': 'create_user'})

__all__ = ['create_user_view']
