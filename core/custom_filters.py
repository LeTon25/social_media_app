from django import template
from django.utils.translation import gettext as _
from django.utils.timesince import timesince as django_timesince

register = template.Library()

@register.filter
def custom_timesince(value, default="trước"):
    if not value:
        return ""
    
    # Gọi hàm timesince của Django với thời gian hiện tại và giá trị được cung cấp
    timesince_str = django_timesince(value).split(', ')[0]
    
    # Tạo một từ điển để dịch các đơn vị thời gian từ tiếng Anh sang tiếng Việt
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
    
    # Tách số và đơn vị thời gian
    number, unit = timesince_str.split()
    
    # Dịch đơn vị thời gian sang tiếng Việt
    translated_unit = translations.get(unit, unit)
    
    # Trả về chuỗi đã được dịch
    return f"{number} {translated_unit} {default}"