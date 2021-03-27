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


BASE_URL = settings.DOC_SERVICE_BASE_API_URL


PATHS = {
    'get_docs_info': '/internal/doctors/list/'
}


def get_url(name):
    return urljoin(BASE_URL, PATHS[name])


@handle_exceptions
def get_docs_info(doc_ids):
    if not doc_ids:
        return []

    url = get_url('get_docs_info')
    response = session.post(url, data={'doc_ids': doc_ids})
    return response.json()['results']
