from django import template
import contracts.models as model


register = template.Library()

@register.simple_tag(name='somth')
def do_anything():
    # Тут буду делать свои теги
    pass

@register.inclusion_tag('contracts/pretension_status.html', name='pretension_status')
def get_pretension_status():
    pass
