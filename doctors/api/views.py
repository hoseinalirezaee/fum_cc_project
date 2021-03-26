from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from common.authentication import CustomTokenAuthentication
from rest_framework import serializers
from api import models
from rest_framework.response import Response
from rest_framework import status


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


create_comment_view = CommentView.as_view()
