import logging
from datetime import datetime
from os import urandom, path
from pytz import utc
from typing import Optional
import re

from rest_framework.response import Response
from ipware.ip import get_ip
from django.conf import settings

from .exceptions import *

logger = logging.getLogger('django')


def get_logger(name: Optional[str] = 'django') -> logging.Logger:
    return logging.getLogger(name)


def get_now() -> datetime:
    return datetime.now(tz=utc)


def response_error(ex, status_code=400):
    print(ex)
    if not isinstance(ex, GenericException):
        ex = GenericException(message=str(ex), status_code=status_code)
    error_message = "Oops! We hit a snag. Please try again in a bit."
    if ex.verbose is True:
        error_message = str(ex)

    error_data = {'code': ex.code, 'message': error_message, 'summary': ex.summary}
    return Response(data=error_data, status=ex.status_code)


def generate_password(length=20) -> str:
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    re = []
    for c in urandom(length - 1):
        t = chars[int(c) % len(chars)]
        l = len(re)
        if l % 2 == 0:
            t = t.lower()

        if l == int(length/2):
            re.append("@")

        re.append(t)

    return "".join(re)


def is_number(s: Optional[str]) -> bool:
    try:
        if s is None:
            return False
        float(str(s))  # for int, long and float
    except ValueError:
        return False
    return True


def is_production() -> bool:
    return settings.ENVIRONMENT == 'production'


def get_app_version(request) -> Optional[str]:
    if not request or not hasattr(request, 'META') or not isinstance(request.META, dict):
        return None
    return request.META.get('HTTP_APP_VERSION')


def get_device_id(request) -> Optional[str]:
    if not request or not hasattr(request, 'META') or not isinstance(request.META, dict):
        return None
    return request.META.get('HTTP_DEVICE_ID')


def get_ip_address(request) -> str:
    return get_ip(request)


def get_static_url(path: str) -> str:
    url = f'{settings.STATIC_URL}{path}'
    return get_absolute_url(url)


def get_media_url(path: str) -> str:
    url = f'{settings.MEDIA_URL}{path}'
    return get_absolute_url(url)


def get_absolute_url(url: str) -> str:
    if re.match(r'^https?:\/\/', url):
        return url
    base_url = str(settings.BASE_URL).rstrip('/')
    return f'{base_url}/{url.lstrip("/")}'


def get_absolute_url_adapter(request, url, **kwargs):
    if re.match(r'^https?:\/\/', url):
        return url
    scheme = request.is_secure() and "https://" or "http://"
    kwargs = kwargs or {}
    url = ''.join([scheme, request.get_host(), settings.MEDIA_URL, url])
    if kwargs:
        url += '?'
        for key, value in kwargs.items():
            if value:
                url = '{}{}={}&'.format(url, key, value)
        url = url.rstrip('&')
    return url


def storage_path(folder, filename):
    path_url = [folder, path.basename(filename)]
    return path.join(*path_url)
