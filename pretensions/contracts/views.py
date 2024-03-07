from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Provider, Contract

menu = [
    {'title': 'Все договоры', 'url_name': 'home'},
    {'title': ' Контрагенты', 'url_name': 'providers'},
    {'title': 'Что-то еще', 'url_name': 'home'},
]

# menu = ['Все договоры', 'Незаполненные договоры', 'Просрочена поставка', 'Новая поставка', 'Требуется инициирование ПИР']

def index(request):
    queryset = Contract.objects.all()
    for contr in queryset:
        contr.make_contract_penalty()
    data = {
        'title': 'Главная страница1',
        'menu': menu,
        'contracts': queryset
    }
    template = 'contracts/index.html'
    return render(request, template, context=data)
    # t = render_to_string('contracts/index.html')
    # return HttpResponse(t)


def providers(request):
    queryset = Provider.objects.all()
    data = {
        'title': 'Поставщики',
        'providers': queryset,
        'menu': menu
    }
    template = 'contracts/providers.html'
    return render(request, template, context=data)


def provider(request, prov_id):
    provider = Provider.objects.get(pk=prov_id)
    data = {
        'title': provider.cut_name,
        'provider': provider,
        'menu': menu
    }
    template = 'contracts/provider.html'
    return render(request, template, context=data)