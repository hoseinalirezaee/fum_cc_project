from django.views.generic.base import TemplateView


class APIDocumentView(TemplateView):
    template_name = 'documents/swagger_template.html'


api_documents_view = APIDocumentView.as_view()

__all__ = ['api_documents_view']
