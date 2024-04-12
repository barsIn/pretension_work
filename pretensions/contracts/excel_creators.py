import pandas as pd
from .models import Contract, Company, Provider, Deliver
from datetime import timedelta


def get_company(number):
    if number[0] == 'B':
        return Company.objects.get(cut_name='ООО "РН-Ванкор"')
    elif number[0:4] == '171':
        return Company.objects.get(cut_name='АО "Ванкорнефть"')
    elif number[0:4] == '751':
        return Company.objects.get(cut_name='АО "Сузун"')
    elif number[0:4] == '752':
        return Company.objects.get(cut_name='ООО "Тагульское"')


def add_contracts(new_file, staff):

    def create_contract(colums, *args):
        number = colums['Номер договора']
        start_date = colums['Дата начала']
        finish_date = colums['Крайняя дата поставки']
        contract_provider = Provider.objects.get(sap_code=colums['Код поставщика'])
        company = get_company(number)
        employee = args[0]
        delivery_item = colums['Предмет поставки']
        amount = colums['Сумма договора']
        payment_term = colums['Срок оплаты']
        remains_deliver_amount = amount
        contract = Contract(number=number,
                            start_date=start_date,
                            finish_date=finish_date,
                            contract_provider=contract_provider,
                            company=company,
                            employee=employee,
                            delivery_item=delivery_item,
                            amount=amount,
                            payment_term=payment_term,
                            remains_deliver_amount=remains_deliver_amount,
                            deliver_penalty_percent=0.03,
                            max_deliver_penalty_percent=100,
                            paid_penalty_percent=0.03,
                            max_paid_penalty_percent=10)
        contract.save()
    data = pd.read_excel(new_file)
    data.apply(create_contract, axis=1, args=(staff,))
    # print(data.info())


def add_provider(new_file):

    def create_provider(colums):
        full_name = colums['Полное наименование']
        cut_name = colums['Сокращенное наименование']
        inn = colums['ИНН']
        sap_code = colums['Код КА в SAP']
        address = colums['Адрес КА']
        e_mail = colums['Электронная почта КА']
        telephone = colums['Телефон']

        contract = Provider(full_name=full_name,
                            cut_name=cut_name,
                            inn=inn,
                            sap_code=sap_code,
                            address=address,
                            e_mail=e_mail,
                            telephone=telephone,
                            )
        contract.save()

    data = pd.read_excel(new_file)
    data.apply(create_provider, axis=1)


def add_deliver(new_file, contract):

    def create_deliver(colums, contract):
        invoice = colums['№ Счета-фактуры/УПД']
        invoice_date = colums['Дата фактуры/УПД']
        total = colums['Сумма поставки']
        delivered = colums['Дата поставки']
        contract = contract
        pay_days = contract.payment_term
        payment_term = delivered + timedelta(days=pay_days)
        deliver = Deliver(invoice=invoice,
                          invoice_date=invoice_date,
                          total=total,
                          delivered=delivered,
                          contract=contract,
                          payment_term=payment_term
                          )
        deliver.save()
    data = pd.read_excel(new_file)
    data.apply(create_deliver, axis=1, args=(contract, ))