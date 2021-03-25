from rest_framework import exceptions, serializers, status
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


class UserViewSet(GenericViewSet):

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
        serializer.save()
        del serializer.validated_data['password']
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    def add_favorite_doctor(self, request, *args, **kwargs):
        if request.user:
            doc_id = request.data.get('doc_id')
            if not doc_id:
                raise exceptions.ValidationError('doc_id is required.', 'required')
            request.user.add_favorite_doctor(doc_id)
        return Response({'message': 'Saved successfully.'})


create_user_view = UserViewSet.as_view(actions={'post': 'create_user'})
add_favorite_doc = UserViewSet.as_view(actions={'post': 'add_favorite_doctor'})

__all__ = ['create_user_view', 'add_favorite_doc']
