from django import template

register = template.Library()

def dict_value(in_dict, key):
    if key in in_dict: return in_dict[key]
    else: return None

register.filter('dict_value', dict_value)

