from django.urls import path

from api import views

urlpatterns = [
    path('get_token/', view=views.get_token_view)
]
