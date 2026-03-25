from django import template
from common.permissions import can_with_perm, has_perm

register = template.Library()

@register.simple_tag
def can_do(user, obj, perm_name, owner_attr='owner'):
    return can_with_perm(user, obj, perm_name, owner_attr)

@register.simple_tag
def user_has_perm(user, perm_name):
    return has_perm(user, perm_name)