import os
import django
from django.db.models import Q, Avg, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import *


def get_directors(search_name=None, search_nationality=None):
    if not (search_name or search_nationality):
        return ""

    query = Q()

    if search_name:
        query &= Q(full_name__icontains=search_name)

    if search_nationality:
        query &= Q(nationality__icontains=search_nationality)

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ""

    ordered_directors = []

    for director in directors:
        ordered_directors.append(
            f"Director: {director.full_name}, "
            f"nationality: {director.nationality}, "
            f"experience: {director.years_of_experience}")

    return '\n'.join(ordered_directors)


def get_top_director():
    director = Director.objects.get_directors_by_movies_count().first()

    if not director:
        return ""

    return f"Top Director: {director.full_name}, movies: {director.num_movies}."


def get_top_actor():
    actor = Actor.objects.prefetch_related('movies').annotate(
        num_movies=Count('movies__starring_actor'),
        avg_movies_rating=Avg('movies__rating')
    ).order_by('-num_movies', 'full_name').first()

    if not actor or not actor.num_movies:
        return ""

    actor_movies = ', '.join(m.title for m in actor.movies.all() if m)

    return f"Top Actor: {actor.full_name}, starring in movies: {actor_movies}, " \
           f"movies average rating: {actor.avg_movies_rating:.1f}"


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(
        num_movies=Count('movie')
    ).order_by('-num_movies', 'full_name')[:3]

    if not actors or not actors[0].num_movies:
        return ""

    result = []

    for actor in actors:
        result.append(f"{actor.full_name}, participated in {actor.num_movies} movies")

    return '\n'.join(result)


def get_top_rated_awarded_movie():
    top_movie = Movie.objects\
        .select_related('starring_actor')\
        .prefetch_related('actors')\
        .filter(is_awarded=True)\
        .order_by('-rating', 'title')\
        .first()

    if not top_movie:
        return ""

    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'
    participating_actors = top_movie.actors.order_by('full_name').values_list('full_name', flat=True)
    cast = ', '.join(participating_actors)

    return f"Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating:.1f}. " \
           f"Starring actor: {starring_actor}. Cast: {cast}."


def increase_rating():
    classic_movies = Movie.objects.filter(is_classic=True, rating__lt=10.0)

    if not classic_movies:
        return "No ratings increased."

    num_of_updated_movies = classic_movies.update(rating=F('rating') + 0.1)

    return f"Rating increased for {num_of_updated_movies} movies."
