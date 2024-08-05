from django.core.validators import MinLengthValidator
from django.db import models


class BaseNameMixin(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )

    class Meta:
        abstract = True


class UpdateMixin(models.Model):
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True
