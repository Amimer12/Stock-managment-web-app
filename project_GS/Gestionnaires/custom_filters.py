from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter
def can_view_self(user):
    """
    Return True if the user is in the 'gestionnaire' group.
    """
    if user.is_authenticated:
        return user.groups.filter(name='gestionnaire').exists()
    return False
