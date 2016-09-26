from django import template

from pricetracker.core import get_secret

register = template.Library()

@register.filter(name='dict_get')
def dict_get(dictionary, key):
    return dictionary[key]

@register.filter(name='replace')
def dict_get(list_of_strings):
    for item in list_of_strings:
        item[0].replace("&#39", "")
    return list_of_strings

@register.filter(name='subtract')
def subtract(first, second):
    return str(float(first) - float(second))

@register.filter(name='stubhub_uri')
def construct_uri(event_id, ticket_id):
    query_string = get_secret('STUBHUB_QUERY_STRING')
    url = 'http://stubhub.com/event/%s/%s&ticket_id=%s' % (event_id, query_string, ticket_id)
    return url

