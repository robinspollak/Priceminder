from django import template

register = template.Library()

@register.filter(name='dict_get')
def dict_get(dictionary, key):
    return dictionary[key]

@register.filter(name='replace')
def dict_get(list_of_strings):
    for item in list_of_strings:
        item[0].replace("&#39", "")
    return list_of_strings
