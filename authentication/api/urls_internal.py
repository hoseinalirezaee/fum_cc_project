from django.urls import path

from api import views

urlpatterns = [
    path('users/<uuid:user_id>/rule/', view=views.get_rule_view),
    path('users/create/', view=views.register_view)
]
