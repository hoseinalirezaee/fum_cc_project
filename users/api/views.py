from rest_framework import exceptions, permissions, serializers, status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api import models


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)
    first_name = serializers.CharField(max_length=64)
    last_name = serializers.CharField(max_length=64)

    def create(self, validated_data):
        user = models.User.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'phone')


class UserViewSet(UpdateModelMixin, GenericViewSet):

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.action == 'create_user':
            return UserCreateSerializer
        return super().get_serializer_class()

    def perform_authentication(self, request):
        if self.action == 'create_user':
            return
        super().perform_authentication(request)

    def get_permissions(self):
        if self.action == 'create_user':
            return []
        return super().get_permissions()

    def create_user(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        del serializer.validated_data['password']
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    @staticmethod
    def _favorite_doc_action(request, method_name):
        if request.user:
            doc_id = request.data.get('doc_id')
            if not doc_id:
                raise exceptions.ValidationError('doc_id is required.', 'required')
            if getattr(request.user, method_name)(doc_id):
                return Response({'message': 'Saved successfully.'})
            else:
                return Response({'message': 'No suck doctor.', 'success': False}, status=404)
        return Response({'sucess': False, 'message': 'Unknown.'}, status=500)

    def remove_favorite_doctor(self, request):
        return self._favorite_doc_action(request, 'remove_favorite_doctor')

    def add_favorite_doctor(self, request):
        return self._favorite_doc_action(request, 'add_favorite_doctor')

    def list_favorite_doctors(self, request):
        if request.user:
            return Response(request.user.list_favorite_doctors())


create_user_view = UserViewSet.as_view(actions={'post': 'create_user'})

add_favorite_doc = UserViewSet.as_view(actions={'post': 'add_favorite_doctor'})

remove_favorite_doc = UserViewSet.as_view(actions={'delete': 'remove_favorite_doctor'})

list_favorite_doc = UserViewSet.as_view(actions={'get': 'list_favorite_doctors'})

update_user_view = UserViewSet.as_view(actions={'post': 'partial_update'})

__all__ = ['create_user_view', 'add_favorite_doc', 'update_user_view', 'remove_favorite_doc']
