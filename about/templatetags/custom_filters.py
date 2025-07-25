from django import template
from django.utils.safestring import mark_safe
from django.utils.encoding import force_str

register = template.Library()

@register.filter
def safe_linebreaksbr(value):
    try:
        value = force_str(value, errors='ignore')
        return mark_safe(value.replace('\n', '<br>'))
    except Exception:
        return value
