from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from main_app.managers import CustomAstronautManager
from main_app.mixins import BaseNameMixin, UpdateMixin


class Astronaut(BaseNameMixin, UpdateMixin):
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='Phone number must contain only digits.'
            )
        ],
        unique=True
    )

    is_active = models.BooleanField(
        default=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    spacewalks = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    objects = CustomAstronautManager()

    def __str__(self):
        return self.name


class Spacecraft(BaseNameMixin, UpdateMixin):
    manufacturer = models.CharField(
        max_length=100,
    )

    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    weight = models.FloatField(
        validators=[MinValueValidator(0.0)]
    )

    launch_date = models.DateField()

    def __str__(self):
        return self.name


class Mission(BaseNameMixin, UpdateMixin):
    class StatusChoices(models.TextChoices):
        PLANNED = 'Planned'
        ONGOING = 'Ongoing'
        COMPLETED = 'Completed'

    description = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=9,
        choices=StatusChoices.choices,
        default=StatusChoices.PLANNED
    )

    launch_date = models.DateField()

    spacecraft = models.ForeignKey(
        to=Spacecraft,
        on_delete=models.CASCADE,
        related_name='missions',
    )

    astronauts = models.ManyToManyField(
        to=Astronaut,
        related_name='missions_astronauts'
    )

    commander = models.ForeignKey(
        to=Astronaut,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='missions_commander'
    )

    def __str__(self):
        return self.name
