from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
