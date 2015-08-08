from django import template

register = template.Library()

@register.filter
def panel_status(value):
    d = {
        'O': 'panel-warning',
        'C': 'panel-success',
        'A': 'panel-danger',
    }
    return d[value]
