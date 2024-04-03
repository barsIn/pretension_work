from django import template
import contracts.models as model


register = template.Library()

@register.simple_tag(name='somth')
def do_anything():
    # Тут буду делать свои теги
    pass
