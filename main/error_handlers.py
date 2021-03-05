import json

from django.conf import settings
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied, ValidationError as DjangoValidationError
from django.http import (HttpResponseServerError, HttpResponseNotFound, HttpResponseForbidden,
                         Http404, HttpResponseBadRequest)
from django.utils.translation import gettext as _
from rest_framework.exceptions import (PermissionDenied as APIPermissionDenied, NotFound,
                                       APIException, ValidationError as APIValidationError)
from rest_framework.response import Response


def api_exception_handler(exception, context):
    if isinstance(exception, (APIPermissionDenied, DjangoPermissionDenied)):
        return permission_denied_handler()

    if isinstance(exception, (NotFound, Http404)):
        return resource_not_found()

    if isinstance(exception, (APIValidationError, DjangoValidationError)):
        data = {
            'success': False,
            'code': 'validation_error',
            'message': _('Sent data is not in valid format.')
        }
        if settings.DEBUG and isinstance(exception, APIValidationError):
            data['details'] = exception.detail
        return Response(data, status=400, content_type='application/json')

    if isinstance(exception, APIException):
        data = {
            'success': False,
            'code': exception.detail.code,
            'message': exception.detail
        }
        return Response(data, status=exception.status_code, content_type='application/json')

    return None


class ErrorHandler:
    code = None
    message = None
    response_class = None

    def __call__(self, *args, **kwargs):
        data = {
            'success': False,
            'code': self.code,
            'message': self.message
        }
        return self.response_class(json.dumps(data, ensure_ascii=False), content_type='application/json')


class ResourceNotFoundHandler(ErrorHandler):
    code = 'resource_not_found'
    message = _('Requested resource is not found.')
    response_class = HttpResponseNotFound


class BadRequestHandler(ErrorHandler):
    code = 'bad_request'
    message = _('Bad request.')
    response_class = HttpResponseBadRequest


class PermissionDeniedHandler(ErrorHandler):
    code = 'permission_denied'
    message = _('You do not have permission to perform this action.')
    response_class = HttpResponseForbidden


class ServerErrorHandler(ErrorHandler):
    code = 'server_error'
    message = _('An unexpected error has occurred.')
    response_class = HttpResponseServerError


class PathNotFoundHandler(ErrorHandler):
    code = 'path_not_found'
    message = _('The requested resource was not found on this server.')
    response_class = HttpResponseNotFound


resource_not_found = ResourceNotFoundHandler()
bad_request = BadRequestHandler()
permission_denied_handler = PermissionDeniedHandler()
server_error_handler = ServerErrorHandler()
path_not_found_handler = PathNotFoundHandler()
