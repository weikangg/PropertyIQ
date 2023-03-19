# Your template tag in app_name/templatetags/pagination_tags.py

from django import template
from urllib.parse import urlencode


register = template.Library()

@register.simple_tag
def url_replace (request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value

    return dict_.urlencode()