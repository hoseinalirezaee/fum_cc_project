from django.contrib import admin
from django.urls import path

from documents.views import api_documents_view
from main import error_handlers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', api_documents_view)
]

handler500 = error_handlers.server_error_handler

handler404 = error_handlers.path_not_found_handler

handler403 = error_handlers.permission_denied_handler

handler400 = error_handlers.bad_request
