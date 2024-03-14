from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return float(value) * arg

@register.filter(name='format_value')
def format_value(value):
    if float(value) >= 10**9:
        return f'{float(value) / 10**9:.2f}B'
    elif float(value) >= 10**6:
        return f'{float(value) / 10**6:.2f}M'
    elif float(value) >= 10**3:
        return f'{float(value) / 10**3:.2f}K'
    else:
        return float(value)

@register.filter
def extract(value, arg):
    return float(value) - float(arg)

@register.filter
def division(value, arg):
    return float(value) / float(arg)