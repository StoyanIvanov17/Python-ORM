import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import *
from django.db.models import Q, Count, F


def get_profiles(search_string=None):
    if search_string is None:
        return ""

    query = Profile.objects.filter(
        Q(full_name__icontains=search_string)
        |
        Q(email__icontains=search_string)
        |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if not query:
        return ""

    return '\n'.join(
        f"Profile: {q.full_name}, email: {q.email}, phone number: {q.phone_number}, orders: {q.orders.count()}"
        for q in query
    )


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if not profiles:
        return ""

    return '\n'.join(
        f"Profile: {p.full_name}, orders: {p.num_orders}"
        for p in profiles
    )


def get_last_sold_products():
    last_order = Order.objects.prefetch_related('products').order_by('products__name').last()

    if last_order is None or not last_order.products.exists():
        return ""

    product_names = [p.name for p in last_order.products.all()]

    return f"Last sold products: {', '.join(product_names)}"


def get_top_products():
    top_products = Product.objects.annotate(
        times_sold=Count('order')
    ).filter(times_sold__gt=0).order_by('-times_sold', 'name')[:5]

    if not top_products:
        return ""

    products_info = [f"{p.name}, sold {p.times_sold} times" for p in top_products]

    return f"Top products:\n" + '\n'.join(products_info)


def apply_discounts():
    orders = Order.objects.annotate(products_available=Count('products')) \
        .filter(products_available__gt=2, is_completed=False) \
        .update(total_price=F('total_price') * 0.9)

    return f"Discount applied to {orders} orders."


def complete_order():
    order = Order.objects.prefetch_related('products').filter(
        is_completed=False
    ).order_by(
        'creation_date'
    ).first()

    if not order:
        return ""

    for product in order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False

        product.save()

    order.is_completed = True
    order.save()

    return 'Order has been completed!'
