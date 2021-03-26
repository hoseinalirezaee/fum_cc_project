import enum
from functools import wraps
from urllib.parse import urljoin

import requests
from django.conf import settings


class UserRule(enum.Enum):
    PATIENT = 'PATIENT'
    DOCTOR = 'DOCTOR'


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
    'get_user_type': '/internal/users/%s/rule/'
}


def get_url(name):
    return urljoin(BASE_URL, PATHS[name])


@handle_exceptions
def get_rule(user_id):
    url = get_url('get_user_type') % user_id
    response = session.get(url)
    return UserRule(response.json()['rule'])


__all__ = ['get_rule']
