from django import template

register = template.Library()

@register.filter
def div(dividend, divisor):
    try:
        if divisor: return int(dividend) / int(divisor)
    except: return ''
