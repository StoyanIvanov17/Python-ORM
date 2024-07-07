from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.custom_manager import CustomAuthorManager


class Author(models.Model):
    full_name = models.CharField(validators=[MinLengthValidator(3)], max_length=100)

    email = models.EmailField(unique=True)

    is_banned = models.BooleanField(default=False)

    birth_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2005)]
    )

    website = models.URLField(blank=True, null=True)

    objects = CustomAuthorManager()


class Article(models.Model):
    class CategoriesChoices(models.TextChoices):
        TECHNOLOGY = 'Technology'
        SCIENCE = 'Science'
        EDUCATION = 'Education'

    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])

    content = models.TextField(validators=[MinLengthValidator(10)])

    category = models.CharField(
        max_length=10,
        choices=CategoriesChoices.choices,
        default=CategoriesChoices.TECHNOLOGY
    )

    authors = models.ManyToManyField(to=Author, related_name='articles')

    published_on = models.DateTimeField(auto_now_add=True, editable=False)


class Review(models.Model):
    content = models.TextField(validators=[MinLengthValidator(10)])

    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name='reviews')

    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, related_name='reviews')

    published_on = models.DateTimeField(auto_now_add=True, editable=False)
