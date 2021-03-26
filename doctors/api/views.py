from common.authentication import CustomTokenAuthentication
from rest_framework import serializers, status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models


class CommentSerializer(serializers.Serializer):
    text = serializers.CharField()


class CommentView(APIView):
    authentication_classes = [CustomTokenAuthentication]

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


create_comment_view = CommentView.as_view()
list_doctors_views = DoctorListView.as_view()
