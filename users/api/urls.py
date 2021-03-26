from django.urls import path

from api import views

urlpatterns = [
    path('create/', views.create_user_view),
    path('add_favorite_doc/', views.add_favorite_doc),
    path('update/', views.update_user_view)
]