from django.urls import path

from api import views

urlpatterns = [
    path('doctors/list/', view=views.internal_list_doctors)
]
