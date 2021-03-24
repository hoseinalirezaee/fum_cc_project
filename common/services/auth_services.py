from functools import wraps
from urllib.parse import urljoin

import requests
from django.conf import settings


def get_session():
    session = requests.Session()
    session.hooks['response'] = lambda r, *args, **kwargs: r.raise_for_status()
    session.auth = (settings.AUTH_SERVICE_ACCESS_USERNAME, settings.AUTH_SERVICE_ACCESS_PASSWORD)
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


BASE_URL = settings.AUTH_SERVICE_BASE_API_URL


PATHS = {
    'create_user': '/internal/users/create/'
}


def get_url(name):
    return urljoin(BASE_URL, PATHS[name])


user_types = {'doc', 'normal'}


def create_user(username, password, type):
    assert type in user_types
    url = get_url('create_user')
    data = {'username': username, 'password': password, 'type': type}
    response = session.post(url, json=data)
    status = response.json()['code'].lower()
    if status == 'ok':
        return True
    return False


__all__ = ['create_user']
