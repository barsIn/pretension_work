from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Provider, Contract
from django.http import HttpResponseNotFound

menu = [
    {'title': 'Все договоры', 'url_name': 'home'},
    {'title': ' Контрагенты', 'url_name': 'providers'},
    {'title': 'Что-то еще', 'url_name': 'home'},
]

# menu = ['Все договоры', 'Незаполненные договоры', 'Просрочена поставка', 'Новая поставка', 'Требуется инициирование ПИР']


def index(request):
    queryset = Contract.objects.filter(is_done=False)
    for contr in queryset:
        contr.make_contract_penalty()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'contracts': queryset
    }
    template = 'contracts/index.html'
    return render(request, template, context=data)
    # t = render_to_string('contracts/index.html')
    # return HttpResponse(t)


def show_contract(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    contract.make_already_get_amount()
    data = {
        'title': contract.number,
        'menu': menu,
        'contract': contract
    }
    delivers = contract.deliver_set.all()
    if delivers:
        data['delivers'] = delivers
    template = 'contracts/contract.html'
    return render(request, template, context=data)


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