from django.urls import path

from api import views

urlpatterns = [
    path('create/', views.create_user_view),
    path('favorite_doc/add/', views.add_favorite_doc),
    path('update/', views.update_user_view),
    path('favorite_doc/list/', view=views.list_favorite_doc),
    path('favorite_doc/remove/', view=views.remove_favorite_doc)
]
