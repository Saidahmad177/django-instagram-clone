import random
from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

from shared.models import BaseModel
from django.db import models


USER, ADMIN, MANAGER = ('user', 'admin', 'manager')
WITH_EMAIL, WITH_PHONE_NUM = ('email', 'phone')
NEW, VERIFIED, DONE, UPLOAD_PHOTO = ('new', 'verified', 'done', 'upload_photo')


class CustomUser(AbstractUser, BaseModel):
    USER_ROLES = (
        (USER, USER),
        (ADMIN, ADMIN),
        (MANAGER, MANAGER)
    )
    AUTH_TYPE = (
        (WITH_EMAIL, WITH_EMAIL),
        (WITH_PHONE_NUM, WITH_PHONE_NUM)
    )
    AUTH_STATUS = (
        (NEW, NEW),
        (VERIFIED, VERIFIED),
        (DONE, DONE),
        (UPLOAD_PHOTO, UPLOAD_PHOTO)
    )

    user_roles = models.CharField(max_length=31, choices=USER_ROLES, default=USER)
    auth_type = models.CharField(max_length=31, choices=AUTH_TYPE)
    auth_status = models.CharField(max_length=31, choices=AUTH_STATUS, default=NEW)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=18, unique=True, null=True, blank=True)
    user_img = models.ImageField(upload_to='users_image/', null=True, blank=True,
                                 validators=FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])
                                 )

    def __str__(self):
        return self.username

    def create_verify_code(self, verify_type):
        code = ''.join([str(random.randint(0, 100) % 10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id=self.id,
            code=code,
            verify_type=verify_type,
        )
        return code


EXPIRE_PHONE = 2
EXPIRE_EMAIL = 5


class UserConfirmation(BaseModel):
    TYPE_CHOICES = (
        (WITH_PHONE_NUM, WITH_PHONE_NUM),
        (WITH_EMAIL, WITH_EMAIL),
    )
    code = models.CharField(max_length=4)
    verify_type = models.CharField(max_length=31, choices=TYPE_CHOICES)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='confirmation')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())

    def save(self, *args, **kwargs):
        if self.pk:
            if self.verify_type == WITH_EMAIL:
                self.expiration_time = datetime.now() + timedelta(minutes=EXPIRE_EMAIL)
            else:
                self.expiration_time = datetime.now() + timedelta(minutes=EXPIRE_PHONE)
