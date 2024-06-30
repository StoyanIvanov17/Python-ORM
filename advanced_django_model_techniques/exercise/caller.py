import os

import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from decimal import Decimal
from django.core.exceptions import ValidationError
from main_app.models import Customer, Book, Product, DiscountedProduct, SpiderHero, FlashHero
