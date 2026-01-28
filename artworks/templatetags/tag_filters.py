from django import template

register = template.Library()

@register.filter
def tags_list(tags_queryset):
    return [tag.name for tag in tags_queryset]