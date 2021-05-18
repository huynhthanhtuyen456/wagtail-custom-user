import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils.models import TimeStampedModel
from core.storage_backends import MediaStorage
from core.utils import storage_path
from datetime import datetime
from allauth.utils import generate_unique_username


class UserRole(TimeStampedModel):
    name = models.CharField(max_length=200, blank=False, null=False)
    role = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class User(AbstractUser):

    def avatar_path(self, filename, *args, **kwargs):
        now = datetime.now()
        folder = '/'.join(['user_profile', str(now.year), str(now.month), str(now.day), 'images'])
        return storage_path(folder, filename)

    def video_path(self, filename, *args, **kwargs):
        now = datetime.now()
        folder = '/'.join(['user_profile', str(now.year), str(now.month), str(now.day), 'videos'])
        return storage_path(folder, filename)

    def documents_path(self, filename, *args, **kwargs):
        now = datetime.now()
        folder = '/'.join(['user_profile', str(now.year), str(now.month), str(now.day), 'documents'])
        return storage_path(folder, filename)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_temp = models.BooleanField(default=False)
    is_verified_email = models.BooleanField(default=False)
    role = models.ForeignKey(UserRole, blank=True, null=True, on_delete=models.CASCADE)
    avatar_url = models.ImageField(storage=MediaStorage(), upload_to=avatar_path, blank=True, null=True)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        if self.email:
            email = self.email
            name = "%s %s (%s)" % (self.first_name, self.last_name, email)
        else:
            name = "%s %s" % (self.first_name, self.last_name)
        if not name.strip():
            name = self.username  # "User #%s" % self.pk
        return name

    @property
    def name(self):
        name = "%s %s" % (self.first_name, self.last_name)

        if not name.strip():
            name = self.username  # "User #%s" % self.pk
        return name

    @property
    def id(self):
        return self.user_id

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = generate_unique_username(
                [self.first_name, self.last_name, self.email, self.username, 'user']
            )

        self.first_name = ' '.join(self.first_name.split())
        self.last_name = ' '.join(self.last_name.split())

        if self.role is None:
            role = UserRole.objects.filter(role='normal').first()
            if role:
                self.role = role

        return super(User, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('user_id', 'email')

class ConfirmCode(TimeStampedModel):
    code = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    expire_date = models.DateTimeField(null=True, blank=True)


class UserSetting(TimeStampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    role = models.ForeignKey(UserRole, null=True, blank=True, on_delete=models.CASCADE)
    notice_mail = models.BooleanField(default=True)
    notice_sms = models.BooleanField(default=False)
    notice_fire_base = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'role')
