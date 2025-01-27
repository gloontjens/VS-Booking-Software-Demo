from django import template

register = template.Library()


@register.filter
def tozero(value):
    if value:
        temp = float(str(value).replace(".00",""))
        if str(temp)[-2:] == '.0':
            return int(temp)
        else:
            return int(temp)
        
        
    else:
        return "0"

@register.filter(name="times")
def times(number):
    return range(1, int(number)+1)
