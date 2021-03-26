from django.urls import include, path

from main import error_handlers

urlpatterns = [
    path('users/', include('api.urls'))
]

handler500 = error_handlers.server_error_handler

handler404 = error_handlers.path_not_found_handler

handler403 = error_handlers.permission_denied_handler

handler400 = error_handlers.bad_request
