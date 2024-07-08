import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import *
from django.db.models import Q, Count


def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ""

    query = Q()

    if search_name is not None:
        query &= Q(full_name__icontains=search_name)

    if search_country is not None:
        query &= Q(country__icontains=search_country)

    tennis_players = TennisPlayer.objects.filter(query).order_by('ranking')

    if not tennis_players:
        return ""

    return '\n'.join(
        f"Tennis Player: {t.full_name}, country: {t.country}, ranking: {t.ranking}"
        for t in tennis_players
    )


def get_top_tennis_player():
    top_player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if top_player is None:
        return ""

    return f"Top Tennis Player: {top_player.full_name} with {top_player.num_wins} wins."


def get_tennis_player_by_matches_count():
    top_player = TennisPlayer.objects.annotate(
        most_matches=Count('matches')
    ).order_by('-most_matches', 'ranking').first()

    if top_player is None or top_player.most_matches == 0:
        return ""

    return f"Tennis Player: {top_player.full_name} with {top_player.most_matches} matches played."


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ""

    tournaments = Tournament.objects.prefetch_related('matches') \
        .annotate(num_matches=Count('matches')) \
        .filter(surface_type__icontains=surface) \
        .order_by('-start_date')

    if not tournaments:
        return ""

    return '\n'.join(
        f"Tournament: {t.name}, start date: {t.start_date}, matches: {t.num_matches}"
        for t in tournaments
    )


def get_latest_match_info():
    latest_match = Match.objects.prefetch_related('players') \
        .order_by('-date_played', '-id').first()

    if latest_match is None:
        return ""

    players = latest_match.players.order_by('full_name')
    player1 = players.first().full_name
    player2 = players.last().full_name
    winner = 'TBA' if latest_match.winner is None else latest_match.winner.full_name

    return f"Latest match played on: {latest_match.date_played}, tournament: {latest_match.tournament.name}, " \
           f"score: {latest_match.score}, players: {player1} vs {player2}, " \
           f"winner: {winner}, summary: {latest_match.summary}"


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return 'No matches found.'

    matches = Match.objects.prefetch_related('winner', 'tournament') \
        .filter(tournament__name__exact=tournament_name) \
        .order_by('-date_played')

    if not matches:
        return 'No matches found.'

    return '\n'.join(
        f"Match played on: {m.date_played}, score: {m.score}, winner: {'TBA' if not m.winner else m.winner.full_name}"
        for m in matches
    )
