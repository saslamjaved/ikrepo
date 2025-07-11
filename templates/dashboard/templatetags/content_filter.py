# blog/templatetags/content_filters.py

from django import template
from django.utils.html import strip_tags

register = template.Library()

@register.filter
def truncate_words(value, arg):
    """
    Truncates a string after a certain number of words.
    """
    try:
        length = int(arg)
    except ValueError:
        return value
    
    words = value.split()
    if len(words) > length:
        return ' '.join(words[:length]) + '...'
    return value
