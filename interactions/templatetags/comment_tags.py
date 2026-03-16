from django import template


register = template.Library()

@register.filter
def is_liked(comment, user):
    return comment.likes.filter(user=user).exists()