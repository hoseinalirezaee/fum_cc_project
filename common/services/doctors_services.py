from functools import wraps
from urllib.parse import urljoin

import requests
from django.conf import settings


def get_session():
    session = requests.Session()
    session.hooks['response'] = lambda r, *args, **kwargs: r.raise_for_status()
    session.auth = (settings.DOC_SERVICE_ACCESS_USERNAME, settings.DOC_SERVICE_ACCESS_PASSWORD)
    return session


session = get_session()


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException:
            return None

    return wrapper


BASE_URL = settings.DOC_SERVICE_BASE_URL


PATHS = {
    'is_doctor': '/internal/docs/exists/'
}


def get_url(name):
    return urljoin(BASE_URL, PATHS[name])


@handle_exceptions
def is_doctor(doc_id):
    url = get_url('is_doctor')
    response = session.get(url, data={'doc_id': doc_id})
    return response.json()['exists']


__all__ = ['is_doctor']
