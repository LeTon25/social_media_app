from django import template
from django.utils.translation import gettext as _
from django.utils.timesince import timesince as django_timesince

register = template.Library()

@register.filter
def custom_timesince(value, default="trước"):
    if not value:
        return ""
    
    timesince_str = django_timesince(value).split(', ')[0]
    
    translations = {
        'minute': 'phút',
        'hour': 'giờ',
        'day': 'ngày',
        'week': 'tuần',
        'month': 'tháng',
        'year': 'năm',
        'minutes': 'phút',
        'hours': 'giờ',
        'days': 'ngày',
        'weeks': 'tuần',
        'months': 'tháng',
        'years': 'năm',
    }
    
    number, unit = timesince_str.split()
    
    translated_unit = translations.get(unit, unit)
    
    return f"{number} {translated_unit} {default}"