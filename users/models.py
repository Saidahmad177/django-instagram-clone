from django.contrib.auth.models import AbstractUser
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
    user_img = models.ImageField(upload_to='users_image/', null=True, blank=True)

    def __str__(self):
        return self.username
