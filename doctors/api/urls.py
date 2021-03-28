from django.urls import path

from api import views

urlpatterns = [
    path('<uuid:doc_id>/comments/', view=views.create_comment_view),
    path('list/', view=views.list_doctors_views),
    path('<uuid:doc_id>/appointments/', view=views.appointment_list_view),
    path('appointments/<int:appointment_id>/reserve/', view=views.reserve_doctor),
    path('users/comments/list/', view=views.user_comments_list),
    path('users/appointments/list/', view=views.user_appointments_list)
]
