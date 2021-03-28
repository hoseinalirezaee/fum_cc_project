from common.authentication import CustomTokenAuthentication
from rest_framework import (exceptions, generics, mixins, permissions,
                            serializers, status, viewsets)
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models


class CommentSerializer(serializers.Serializer):
    text = serializers.CharField()


class CommentView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, doc_id):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor = get_object_or_404(models.Doctor.objects.all(), id=doc_id)
        comment = models.Comment.create_comment(doctor, request.user.user_id, serializer.validated_data['text'])
        data = {
            'text': comment.text,
            'date_added': comment.date_added,
            'doc_id': comment.doctor.id,
            'user_id': comment.patient_id
        }
        return Response(data, status=status.HTTP_201_CREATED)


class DoctorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Doctor
        fields = ['id', 'first_name', 'last_name', 'phone', 'address', 'men', 'expertise', 'city']


class DoctorListView(ListAPIView):
    queryset = models.Doctor.objects.all()
    serializer_class = DoctorListSerializer

    def perform_authentication(self, request):
        pass


class DoctorListInternal(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.Doctor.objects.all()
    serializer_class = DoctorListSerializer

    def perform_authentication(self, request):
        pass

    def filter_queryset(self, queryset):
        doc_ids = self.request.data.get('doc_ids')
        if doc_ids is None or not isinstance(doc_ids, list):
            raise exceptions.ValidationError('doc_ids must be provided and be an instance of list.', 'validation_error')
        return queryset.filter(id__in=doc_ids)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AppointmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppointmentTime
        fields = ['id', 'date', 'time_from', 'time_to']


class AppointmentsList(ListAPIView):

    serializer_class = AppointmentListSerializer

    def perform_authentication(self, request):
        pass

    def get_queryset(self):
        doc_id = self.kwargs.get('doc_id')
        return models.AppointmentTime.objects.filter(doctor_id=doc_id)


class ReserveDoctorView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, appointment_id):
        appointment = get_object_or_404(models.AppointmentTime.objects.all(), id=appointment_id)
        reservation = appointment.reserve(request.user.user_id)
        return Response({'reservation_id': reservation.id}, status=status.HTTP_201_CREATED)


class UserCommentSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField()

    class Meta:
        model = models.Comment
        fields = ['patient_id', 'date_added', 'text', 'doctor']


class UserAppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField()
    appointment = AppointmentListSerializer()

    class Meta:
        model = models.Reservation
        fields = ['id', 'patient_id', 'doctor', 'appointment']


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action == 'get_user_comments':
            return models.Comment.objects.all()

        if self.action == 'get_user_appointments':
            return models.Reservation.objects.all()

        return super().get_queryset()

    def filter_queryset(self, queryset):
        return queryset.filter(patient_id=self.request.user.user_id)

    def get_serializer_class(self):
        if self.action == 'get_user_comments':
            return UserCommentSerializer

        if self.action == 'get_user_appointments':
            return UserAppointmentSerializer

        return super().get_serializer_class()

    def get_user_comments(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_user_appointments(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


create_comment_view = CommentView.as_view()
list_doctors_views = DoctorListView.as_view()
appointment_list_view = AppointmentsList.as_view()
reserve_doctor = ReserveDoctorView.as_view()
internal_list_doctors = DoctorListInternal.as_view()

user_comments_list = UserViewSet.as_view(actions={'get': 'get_user_comments'})
user_appointments_list = UserViewSet.as_view(actions={'get': 'get_user_appointments'})
