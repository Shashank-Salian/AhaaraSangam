from django import template
from django.forms import BoundField
import random

from ..raw_data import QUOTES

register = template.Library()


@register.filter(name="add_classes")
def add_classes(value: BoundField, arg):
    css_classes = value.css_classes().split()
    args = arg.split()
    for a in args:
        if a not in css_classes:
            css_classes.append(a)

    return value.as_widget(attrs={'class': ' '.join(css_classes)})


@register.simple_tag(name="random_quote")
def random_quote():
    return random.choice(QUOTES)
