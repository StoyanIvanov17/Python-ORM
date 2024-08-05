import os
import django
from django.db.models import Q, Count, Sum, F, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import *


def get_astronauts(search_string=None):
    if search_string is None:
        return ""

    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string)
        |
        Q(phone_number__icontains=search_string)
    ).order_by('name')

    if not astronauts:
        return ""

    return '\n'.join(
        f"Astronaut: {a.name}, phone number: {a.phone_number}, status: {'Active' if a.is_active else 'Inactive'}"
        for a in astronauts
    )


def get_top_astronaut():
    astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if not astronaut or astronaut.num_missions == 0:
        return 'No data.'

    return f"Top Astronaut: {astronaut.name} with {astronaut.num_missions} missions."


def get_top_commander():
    astronaut = Astronaut.objects.annotate(
        commanded_missions=Count('missions_commander')
    ).order_by('-commanded_missions', 'phone_number').first()

    if not astronaut or astronaut.commanded_missions == 0:
        return 'No data.'

    return f"Top Commander: {astronaut.name} with {astronaut.commanded_missions} commanded missions."


def get_last_completed_mission():
    mission = Mission.objects\
        .select_related('spacecraft')\
        .prefetch_related('astronauts')\
        .annotate(num_spacewalks=Sum('astronauts__spacewalks'))\
        .filter(status='Completed')\
        .order_by('-launch_date')\
        .first()

    if not mission:
        return 'No data.'

    commander = 'TBA' if not mission.commander else mission.commander.name
    astronauts = ', '.join(a.name for a in mission.astronauts.all().order_by('name'))

    return f"The last completed mission is: {mission.name}. Commander: {commander}. Astronauts: {astronauts}. "\
           f"Spacecraft: {mission.spacecraft.name}. Total spacewalks: {mission.num_spacewalks}."


def get_most_used_spacecraft():
    spacecraft = Spacecraft.objects.annotate(
        num_missions=Count('missions'),
    ).order_by('-num_missions', 'name').first()

    if not spacecraft or spacecraft.num_missions == 0:
        return 'No data.'

    unique_astronauts = Astronaut.objects.filter(missions_astronauts__spacecraft=spacecraft).distinct().count()

    return f"The most used spacecraft is: {spacecraft.name}, manufactured by {spacecraft.manufacturer}, "\
           f"used in {spacecraft.num_missions} missions, astronauts on missions: {unique_astronauts}."


def decrease_spacecrafts_weight():
    spacecrafts = Spacecraft.objects.filter(
        missions__status='Planned',
        weight__gte=200.0
    ).update(weight=F('weight') - 200.0)

    if not spacecrafts:
        return 'No changes in weight.'

    avg_weight = Spacecraft.objects.all().aggregate(
        avg_weight=Avg('weight'))['avg_weight']

    return f"The weight of {spacecrafts} spacecrafts has been decreased. "\
           f"The new average weight of all spacecrafts is {avg_weight}kg"


