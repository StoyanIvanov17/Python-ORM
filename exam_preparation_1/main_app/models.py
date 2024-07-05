from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models

from main_app.managers import DirectorManager
from main_app.mixins import BasePerson, LastUpdated, Awarded


class Director(BasePerson):
    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    objects = DirectorManager()

    def __str__(self):
        return f"Director: {self.full_name}"


class Actor(BasePerson, LastUpdated, Awarded):

    def __str__(self):
        return self.full_name


class Movie(Awarded, LastUpdated):
    class GenreChoices(models.TextChoices):
        ACTION = 'Action'
        COMEDY = 'Comedy'
        DRAMA = 'Drama'
        OTHER = 'Other'

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)]
    )

    release_date = models.DateField()

    storyline = models.TextField(null=True, blank=True)

    genre = models.CharField(
        max_length=6,
        choices=GenreChoices.choices,
        default=GenreChoices.OTHER,
    )

    rating = models.DecimalField(
        max_digits=3, decimal_places=1, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )

    is_classic = models.BooleanField(default=False)

    director = models.ForeignKey(
        to=Director,
        on_delete=models.CASCADE,
        related_name='movies',
    )

    starring_actor = models.ForeignKey(
        to=Actor,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='movies'
    )

    actors = models.ManyToManyField(to=Actor)

    def __str__(self):
        return self.title
