from django.urls import path
from api import views


urlpatterns = [
    path('<uuid:doc_id>/comments/', view=views.create_comment_view)
]
