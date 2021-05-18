from .exceptions import MissedUsernameOrEmailException
from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def exists_user(username=None, email=None):
    if not username and not email:
        raise MissedUsernameOrEmailException()
    if username:
        queryset = User.objects.filter(username__iexact=username)
    else:
        queryset = User.objects.filter(email__iexact=email)
    count = queryset.count()
    return count > 0