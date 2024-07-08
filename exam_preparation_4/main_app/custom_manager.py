from django.db import models
from django.db.models import Count


class CustomTennisPlayerManager(models.Manager):
    def get_tennis_players_by_wins_count(self):
        return self.annotate(
            num_wins=Count('matches_won')
        ).order_by('-num_wins', 'full_name')
