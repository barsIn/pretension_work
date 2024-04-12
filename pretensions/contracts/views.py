from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Provider, Contract, Staff, Deliver, Company
from .forms import AddContractForm, MultiAddForm, AddProviderForm, AddDeliverForm
from .excel_creators import add_contracts, get_company, add_provider, add_deliver
from django.http import HttpResponseNotFound
from datetime import timedelta, datetime

menu = [
    {'title': 'Действующие договоры', 'url_name': 'home'},
    {'title': 'Добавить договор', 'url_name': 'create_contract'},
    {'title': 'Контрагенты', 'url_name': 'providers'},
    {'title': 'Добавить поставщика', 'url_name': 'create_provider'},
    {'title': 'Не заполненные', 'url_name': 'unfielded'},
    {'title': 'Все договоры', 'url_name': 'all_contracts'},
]

# menu = ['Все договоры', 'Незаполненные договоры', 'Просрочена поставка', 'Новая поставка', 'Требуется инициирование ПИР']


def index(request):
    queryset = Contract.unblank.filter(is_done=False)
    for contract in queryset:
        contract.make_already_get_amount()
        contract.make_contract_penalty()
        contract.set_done()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'contracts': queryset
    }
    if Contract.unblank.all().exists():
        data['blank'] = Contract.blanks.count()
    template = 'contracts/index.html'
    return render(request, template, context=data)
    # t = render_to_string('contracts/index.html')
    # return HttpResponse(t)


def all_contracts(request):
    queryset = Contract.unblank.all()
    data = {
        'title': 'Все договоры',
        'menu': menu,
        'contracts': queryset
    }
    if Contract.unblank.all().exists():
        data['blank'] = Contract.blanks.count()
    template = 'contracts/index.html'
    return render(request, template, context=data)


def unfilded_contracts(request):
    queryset = Contract.blanks.all()
    data = {
        'title': 'Не заполненные договоры',
        'menu': menu,
        'contracts': queryset
    }
    template = 'contracts/index.html'
    return render(request, template, context=data)


def show_contract(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    if contract.company is None:
        contract.set_company()
    contract.make_contract_penalty()
    contract.make_already_get_amount()
    status = contract.pretension_status
    data = {
        'title': contract.number,
        'menu': menu,
        'contract': contract,
        'status': Contract.PRETENSION_CHOICES[status]
    }
    delivers = contract.deliver.all()
    if delivers:
        data['delivers'] = delivers
    template = 'contracts/contract.html'
    return render(request, template, context=data)


def create_contract(request):
    if request.method == 'POST':
        id = request.user.id
        staff = Staff.objects.get(user__id=id)
        if request.FILES:
            mform = MultiAddForm(request.POST, request.FILES)
            if mform.is_valid():
                add_contracts(request.FILES['multy_add'], staff)
                return redirect('home')
        else:
            form = AddContractForm(request.POST)
            if form.is_valid():
                try:
                    form.cleaned_data['contract_provider'] = Provider.objects.get(sap_code=form.cleaned_data['contract_provider'])
                    form.cleaned_data['employee'] = staff
                    form.cleaned_data['company'] = get_company(form.cleaned_data['number'])
                    form.cleaned_data['remains_deliver_amount'] = form.cleaned_data['amount']
                    Contract.objects.create(**form.cleaned_data)
                    return redirect('home')
                except Exception as e:
                    print(e)
                    form.add_error(None, "Договор не добавлен")
            data = {
                'title': 'Создание договора',
                'menu': menu,
                'form': form,
            }
    else:
        form = AddContractForm()
        mform = MultiAddForm()
        data = {
            'title': 'Создание договора',
            'menu': menu,
            'form': form,
            'mform': mform
        }
    template = 'contracts/create_contract.html'
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
    provider = get_object_or_404(Provider, pk=prov_id)
    data = {
        'title': provider.cut_name,
        'provider': provider,
        'menu': menu
    }
    template = 'contracts/provider.html'
    return render(request, template, context=data)


def create_provider(request):
    if request.method == 'POST':
        if request.FILES:
            mform = MultiAddForm(request.POST, request.FILES)
            form = AddProviderForm()
            if mform.is_valid():
                add_provider(request.FILES['multy_add'])
                return redirect('providers')
        else:
            form = AddProviderForm(request.POST)
            mform = MultiAddForm()
            if form.is_valid():
                form.save()
                return redirect('providers')
        data = {
            'title': 'Создание поставщика',
            'menu': menu,
            'form': form,
            'mform': mform
        }
    else:
        form = AddProviderForm()
        mform = MultiAddForm()
        data = {
            'title': 'Создание поставщика',
            'menu': menu,
            'form': form,
            'mform': mform
        }
    template = 'contracts/create_provider.html'
    return render(request, template, context=data)


def create_deliver(request, contract_id):
    contract = Contract.objects.get(pk=contract_id)
    if request.method == 'POST':
        if request.FILES:
            mform = MultiAddForm(request.POST, request.FILES)
            form = AddProviderForm()
            if mform.is_valid():
                add_deliver(request.FILES['multy_add'], contract)
                return redirect('contract_id', contract_id)
        else:
            form = AddDeliverForm(request.POST)
            mform = MultiAddForm()
            if form.is_valid():
                pay_days = contract.payment_term
                payment_term = form.cleaned_data['invoice_date'] + timedelta(days=pay_days)
                form.cleaned_data['payment_term'] = payment_term
                form.cleaned_data['contract'] = contract
                Deliver.objects.create(**form.cleaned_data)
                # form.save()
                return redirect('contract_id', contract_id)
        data = {
            'title': 'Создание поставщика',
            'menu': menu,
            'form': form,
            'mform': mform
        }
    else:
        form = AddDeliverForm()
        mform = MultiAddForm()
        data = {
            'title': 'Создание поставщика',
            'menu': menu,
            'form': form,
            'mform': mform
        }
    template = 'contracts/create_provider.html'
    return render(request, template, context=data)