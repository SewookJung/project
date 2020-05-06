from django import template
from django.template import Template

register = template.Library()


@register.simple_tag
def assign_value(str=None):
    return str
