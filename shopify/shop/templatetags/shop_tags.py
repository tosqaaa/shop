from django import template
from shop.models import Category

register = template.Library()


@register.inclusion_tag(filename='shop/inc/_list_categories.html')
def list_categories():
    categories = Category.objects.all()
    return {'categories': categories}
