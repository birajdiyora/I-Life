# app/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def file_url(photo, size):
    return photo.file_url(size)
