from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Provider(models.Model):
    # Модель поставщика
    full_name = models.CharField(max_length=200)
    cut_name = models.CharField(max_length=50)
    inn = models.IntegerField(unique=True)
    sap_code = models.IntegerField(unique=True)
    address = models.TextField()
    e_mail = models.EmailField()
    telephone = models.CharField(max_length=20)
    penalty_for_supply = models.FloatField(default=0.0)
    penalty_for_payment = models.FloatField(default=0.0)
    total_penalty = models.FloatField(default=0.0)
    payd_penalty = models.FloatField(default=0.0)
    sum_of_pretensions = models.FloatField(default=0.0)

    def __str__(self):
        return self.cut_name

    def get_sum_of_pretensions(self):
        # Возвращает сумму выставленных претензий
        pass

    def get_payd_penalty(self):
        # Возвращает оплаченную неустойку
        pass

    def get_total_penalty(self):
        # Итого нестойки + или -
        pass

    def get_penalty_for_payment(self):
        # Возвращает сумму неустойки за оплату
        pass

    def get_penalty_for_supply(self):
        # Возвращает сумму неустойки за поставку
        pass

    def get_contracts_count(self):
        # Возвращает количество догооров
        pass

    def get_bad_history(self):
        # Возвращает количество (или процент) договоров с просрочкой поставки
        pass


class Contract(models.Model):
    UNINITIATED = 'UI'
    BEFORPRETENSION = 'BP'
    PRETENSION_NOTE = 'PN'
    PRETENSION = 'PT'
    LAWSUIT_NOTE = 'LN'
    LAWSUIT_START = 'LS'
    LAWSUIT_FINISH = 'LF'
    STPTED_BY_MANAGMENT = 'SM'
    FINISHED = 'FN'
    PRETENSION_CHOICES = {
        UNINITIATED: 'Не инициирована',
        BEFORPRETENSION: 'Допретензионное направлено',
        PRETENSION_NOTE: 'Направлена СЗ на претензию',
        PRETENSION: 'Направлена претензия',
        LAWSUIT_NOTE: 'Направлена СЗ по исковому',
        LAWSUIT_START: 'Иск подан в суд',
        LAWSUIT_FINISH: 'Суд завершен',
        STPTED_BY_MANAGMENT: 'Прекращено руководством',
        FINISHED: 'Завершена'
    }
    # Модель договора
    number = models.CharField(max_length=16, unique=True)
    start_date = models.DateField(blank=True)
    finish_date = models.DateField(blank=True, null=True)  # Крайняя дата поставки
    contract_provider = models.ForeignKey(
        Provider,
        on_delete=models.PROTECT
    )
    company = models.ForeignKey('Company', on_delete=models.CASCADE, blank=True, null=True)  # Это общество группы с которым заключен договор
    employee = models.ForeignKey('Staff', on_delete=models.PROTECT, blank=True)
    delivery_item = models.CharField(max_length=200, blank=True)  # Предмет поставки
    amount = models.FloatField()  # Сумма договора
    payment_term = models.IntegerField(null=True, default=60)  # Срок оплаты в днях
    deliver_penalty_percent = models.FloatField(blank=True, null=True)
    max_deliver_penalty_percent = models.FloatField(blank=True, null=True)
    paid_penalty_percent = models.FloatField(blank=True, null=True)
    max_paid_penalty_percent = models.FloatField(blank=True, null=True)
    already_get_amount = models.FloatField(default=0.0)
    remains_deliver_amount = models.FloatField(blank=True)
    penalty_for_supply = models.FloatField(default=0.0)
    penalty_for_payment = models.FloatField(default=0.0)
    sum_of_pretensions = models.FloatField(default=0.0)
    pretension_status = models.CharField(
        max_length=2,
        choices=PRETENSION_CHOICES,
        default=UNINITIATED
    )
    paid_penalty = models.FloatField(default=0.0)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f'Договор {self.number} от {self.start_date} на сумму {self.amount} р'

    def save(self, *args, **kwargs):
        self.remains_deliver_amount = self.amount
        super(Contract, self).save(*args, **kwargs)

    def make_already_get_amount(self):
        #  Расчитывает сумму поставленного и изменяет значение остатка к поставке
        already_amount = 0
        all_delivers = self.deliver_set.all()
        if all_delivers:
            for deliver in all_delivers:
                already_amount += deliver.total
            self.already_get_amount = already_amount
            self.remains_deliver_amount = self.amount - already_amount

    def make_contract_penalty(self):
        # Расчитывает неустойку и выдает итого неустойки + или -
        Contract.make_already_get_amount(self)
        all_delivers = self.deliver_set.all()
        penalty_for_supply = 0
        penalty_for_payment = 0
        if all_delivers:
            for deliver in all_delivers:
                deliver_late_days = (deliver.delivered-self.finish_date).days #  Дней просрочки поставки
                #  Вычислим дней по просрочки оплаты
                if deliver.paid_fact:
                    paid_late_days = (deliver.paid_fact - (deliver.delivered + datetime.timedelta(days=self.payment_term))).days
                else:
                    paid_late_days = (datetime.date.today() - (deliver.delivered + datetime.timedelta(days=self.payment_term))).days
                #   Вычислим пеню за просрочку поставки
                if deliver_late_days > 0:
                    penalty_for_supply += (deliver.total / 100) * self.deliver_penalty_percent * deliver_late_days
                #  Вычислим неустойку за просрочку оплаты
                if paid_late_days > 0:
                    penalty_for_payment += (deliver.total / 100) * self.paid_penalty_percent * paid_late_days
        if self.remains_deliver_amount > 0:
            deliver_late_days = (datetime.date.today()-self.finish_date).days
            penalty_for_supply += self.remains_deliver_amount / 100 * self.paid_penalty_percent * deliver_late_days
        #  Далее считаем максимальные неустойки по договору
        deliver_max_penalty = self.amount / 100 * self.max_deliver_penalty_percent
        payment_max_penalty = self.amount / 100 * self.max_paid_penalty_percent

        if penalty_for_supply > deliver_max_penalty:
            penalty_for_supply = deliver_max_penalty
        if penalty_for_payment > payment_max_penalty:
            penalty_for_payment = payment_max_penalty
        self.penalty_for_payment = penalty_for_payment
        self.penalty_for_supply = penalty_for_supply
        self.sum_of_pretensions = penalty_for_supply - penalty_for_payment
        return penalty_for_supply - penalty_for_payment

    def get_penalty_for_payment(self):
        return self.penalty_for_payment

    def get_penalty_for_supply(self):
        return self.penalty_for_supply

    def set_pretension_status(self):
        # Устанавливает статус претензионный статус договора
        pass

    def set_done(self):
        # Устанавливает статус закрытого договора если всё поставлено без пени, либо если претензионка прекращена,
        # либо претензионка не инициирована и срок исковой давности истек
        pass

    def set_company(self):
        # Учтанавлиывет компанию по номеру договора
        pass


class Company(models.Model):
    # Это общество группы от имени которого заключался договор
    full_name = models.CharField(max_length=200)
    cut_name = models.CharField(max_length=50)
    inn = models.IntegerField(unique=True)
    sap_code = models.IntegerField(unique=True)
    address = models.TextField()
    e_mail = models.EmailField()
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.cut_name


class Department(models.Model):
    # Отдел
    title = models.CharField(max_length=72)
    cut = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Staff(models.Model):
    # Персонал
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sap_id = models.IntegerField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    dep_director = models.BooleanField(default=False)  # Является ли начальником отдела
    main_man = models.BooleanField(default=False)  # Является ли руководителем верхнего звена

    def __str__(self):
        return self.user.username


class Deliver(models.Model):
    # Поставка товара на сумму по договору
    invoice = models.CharField(max_length=128)  # № счет-фактуры (УПД)
    invoice_date = models.DateField()  # Дата фактуры
    total = models.FloatField()  #Сумма фактуры
    delivered = models.DateField(blank=True, null=True)
    payment_term = models.DateField(blank=True, null=True)  # срок оплаты дата
    paid_fact = models.DateField(blank=True, null=True)  # факт оплаты дата
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

    def __str__(self):
        return f'Поставка {self.invoice} от {self.invoice_date}  сумма {self.total} по договору {self.contract.number}'

    def set_payment_term(self):
        # Установить срок оплаты
        pass


class BeforePretension(models.Model):
    # Допретензионное требование
    number = models.CharField(max_length=10)
    note_date = models.DateField()
    penalty_amount = models.FloatField()
    letter_image = models.FileField(upload_to="beforepretension/%Y/%m/%d/%s")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    have_answer = models.BooleanField(default=False)
    answer_image = models.FileField(upload_to="beforepretension/answers/%Y/%m/%d/%s", blank=True)
    is_satisfied = models.BooleanField(default=False)
    penalty_paid = models.FloatField(default=0)

    def __str__(self):
        return f'№ {self.number} от {self.note_date}'


class PretensionNote(models.Model):
    # СЗ на УПОБ об инициировании претензии
    number = models.CharField(max_length=10)
    note_date = models.DateField()
    penalty_amount = models.FloatField()
    letter_image = models.FileField(upload_to="pretension_note/%Y/%m/%d/%s")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    have_answer = models.BooleanField(default=False)
    answer_image = models.FileField(upload_to="pretension_note/answers/%Y/%m/%d/%s", blank=True)

    def __str__(self):
        return f'№ {self.number} от {self.note_date}'


class Pretension(models.Model):
    # Претензия
    number = models.CharField(max_length=10)
    note_date = models.DateField()
    penalty_amount = models.FloatField()
    letter_image = models.FileField(upload_to="pretension/%Y/%m/%d/%s")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    have_answer = models.BooleanField(default=False)
    answer_image = models.FileField(upload_to="pretension/answers/%Y/%m/%d/%s", blank=True)
    is_satisfied = models.BooleanField(default=False)
    penalty_paid = models.FloatField(default=0)

    def __str__(self):
        return f'№ {self.number} от {self.note_date}'


class LawsuitNote(models.Model):
    # СЗ на ГД по исковой
    number = models.CharField(max_length=10)
    note_date = models.DateField()
    penalty_amount = models.FloatField()
    letter_image = models.FileField(upload_to="pretension_note/%Y/%m/%d/%s")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    have_answer = models.BooleanField(default=False)
    answer_image = models.FileField(upload_to="pretension_note/answers/%Y/%m/%d/%s", blank=True)

    def __str__(self):
        return f'№ {self.number} от {self.note_date}'


class Lawsuit(models.Model):
    # Иск в суд
    number = models.CharField(max_length=10)
    note_date = models.DateField()
    penalty_amount = models.FloatField()
    letter_image = models.FileField(upload_to="lawsuit/%Y/%m/%d/%s")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    case = models.CharField(max_length=100, blank=True)
    decision_image = models.FileField(upload_to="lawsuit/decision/%Y/%m/%d/%s", blank=True)
    decision_penalty = models.FloatField(blank=True)
    is_satisfied = models.BooleanField(default=False)
    penalty_paid = models.FloatField(default=0)

    def __str__(self):
        return f'№ {self.number} от {self.note_date}'
