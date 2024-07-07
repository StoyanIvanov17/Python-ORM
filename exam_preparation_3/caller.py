import os
import django
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Article


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ""

    query = Q()

    if search_name is not None:
        query &= Q(full_name__icontains=search_name)

    if search_email is not None:
        query &= Q(email__icontains=search_email)

    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors.exists():
        return ""

    return '\n'.join(
        f"Author: {a.full_name}, email: {a.email}, status: {'Banned' if a.is_banned else 'Not Banned'}"
        for a in authors
    )


def get_top_publisher():
    author = Author.objects.get_authors_by_article_count().first()

    if author is None or author.num_articles == 0:
        return ""

    return f"Top Author: {author.full_name} with {author.num_articles} published articles."


def get_top_reviewer():
    reviewer = Author.objects.annotate(
        num_reviews=Count('reviews')
    ).order_by('-num_reviews', 'email').first()

    if reviewer is None or reviewer.num_reviews == 0:
        return ""

    return f"Top Reviewer: {reviewer.full_name} with {reviewer.num_reviews} published reviews."


def get_latest_article():
    article = Article.objects.prefetch_related('authors', 'reviews').order_by('-published_on').first()

    if article is None:
        return ""

    authors = ', '.join(author.full_name for author in article.authors.all().order_by('full_name'))
    times_reviewed = article.reviews.count()
    average_rating = sum(r.rating for r in article.reviews.all()) / times_reviewed if times_reviewed else 0.0

    return f"The latest article is: {article.title}. Authors: {authors}. "\
           f"Reviewed: {times_reviewed} times. Average Rating: {average_rating:.2f}."


def get_top_rated_article():
    top_article = Article.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating', 'title').first()

    num_reviews = top_article.reviews.count() if top_article else 0.0

    if top_article is None or num_reviews == 0:
        return ""

    return f"The top-rated article is: {top_article.title}, with an average rating of {top_article.avg_rating:.2f}, " \
           f"reviewed {num_reviews} times."


def ban_author(email=None):
    author = Author.objects.prefetch_related('reviews').filter(email__exact=email).first()

    if email is None or author is None:
        return 'No authors banned.'

    author_reviews = author.reviews.count()

    author.is_banned = True
    author.reviews.all().delete()
    author.save()

    return f"Author: {author.full_name} is banned! {author_reviews} reviews deleted."
