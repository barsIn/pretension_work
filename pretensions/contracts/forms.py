from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible

from .models import Contract, Provider, Deliver


@deconstructible
class ContractValidator:
    needed_lenght = 13
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Неверно указан номер договора"

    def __call__(self, value, *args, **kwargs):
        if len(value) != 13:
            raise ValidationError(self.message, code=self.code)
        elif len(value.split('/')) != 2:
            raise ValidationError(self.message, code=self.code)
        elif value[-1] != 'Д':
            raise ValidationError(self.message, code=self.code)


class AddContractForm(forms.Form):
    number = forms.CharField(max_length=13, label='№ Договора',
                             validators=[ContractValidator()])
    start_date = forms.DateField(label='Дата договора')
    finish_date = forms.DateField(label='Крайняя дата поставки')
    contract_provider = forms.IntegerField(label='Поставщик')
    delivery_item = forms.CharField(max_length=200, label='Предмет договора')
    amount = forms.FloatField(label='Сумма договора')
    payment_term = forms.IntegerField(label='Срок оплаты в днях')


class MultiAddForm(forms.Form):
    # title = forms.CharField(max_length=50)
    multy_add = forms.FileField(label='Файл для множественной загрузки')


class AddProviderForm(forms.ModelForm):

    class Meta:
        model = Provider
        fields = '__all__'
        exclude = ['penalty_for_supply', 'penalty_for_payment', 'total_penalty', 'payd_penalty', 'sum_of_pretensions']
        widgets = {
            'address': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }


class AddDeliverForm(forms.ModelForm):

    class Meta:
        model = Deliver
        fields = ['invoice', 'invoice_date', 'total', 'delivered']
        widgets = {
            "invoice_date": forms.DateInput(format="%d.%m.%Y"),
            "delivered": forms.DateInput(format="%d.%m.%Y"),
        }