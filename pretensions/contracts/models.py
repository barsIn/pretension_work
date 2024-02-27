from django.db import models
from django.contrib.auth.models import User


class Provider(models.Model):
    # Модель поставщика
    full_name = models.CharField(max_length=200)
    cut_name = models.CharField(max_length=50)
    inn = models.IntegerField()
    sap_code = models.IntegerField()
    address = models.TextField()
    e_mail = models.EmailField()
    telephone = models.CharField(max_length=20)
    penalty_for_supply = models.FloatField(default=0.0)
    penalty_for_payment = models.FloatField(default=0.0)
    total_penalty = models.FloatField(default=0.0)
    payd_penalty = models.FloatField(default=0.0)
    sum_of_pretensions = models.FloatField(default=0.0)

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
    number = models.CharField(max_length=9)
    start_date = models.DateField(blank=True)
    finish_date = models.DateField(blank=True) # Крайняя дата поставки
    contract_provider = models.ForeignKey(
        Provider,
        on_delete=models.PROTECT
    )
    company = models.ForeignKey('Company', on_delete=models.CASCADE, blank=True)  # Это общество группы с которым заключен договор
    employee = models.ForeignKey('Staff', on_delete=models.PROTECT, blank=True)
    delivery_item = models.CharField(max_length=200, blank=True)  # Предмет поставки
    amount = models.FloatField(blank=True)  # Сумма договора
    payment_term = models.IntegerField()  # Срок оплаты в днях
    deliver_penalty_percent = models.FloatField(blank=True)
    max_deliver_penalty_percent = models.FloatField(blank=True)
    paid_penalty_percent = models.FloatField(blank=True)
    max_paid_penalty_percent = models.FloatField(blank=True)
    already_get_amount = models.FloatField(default=0.0)
    remains_deliver_amount = models.FloatField(default=amount, blank=True)
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

    def make_already_get_amount(self):
        # Расчитывает сумму поставленного
        pass

    def make_remains_deliver_amount(self):
        # Расчитывает остаток к поставке
        pass

    def get_contract_penalty(self):
        # Итого нестойки + или -
        pass

    def get_penalty_for_payment(self):
        # Возвращает сумму неустойки за оплату
        pass

    def get_penalty_for_supply(self):
        # Возвращает сумму неустойки за поставку
        pass

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
    inn = models.IntegerField()
    sap_code = models.IntegerField()
    address = models.TextField()
    e_mail = models.EmailField()
    telephone = models.CharField(max_length=20)


class Department(models.Model):
    # Отдел
    title = models.CharField(max_length=72)
    cut = models.CharField(max_length=10)


class Staff(models.Model):
    # Персонал
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sap_id = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    dep_director = models.BooleanField(default=False)  # Является ли начальником отдела
    main_man = models.BooleanField(default=False)  # Является ли руководителем верхнего звена


class Deliver(models.Model):
    # Поставка товара на сумму по договору
    invoice = models.CharField(max_length=128)  # № счет-фактуры (УПД)
    invoice_date = models.DateField()  # Дата фактуры
    total = models.FloatField()  #Сумма фактуры
    delivered = models.DateField(blank=True)
    payment_term = models.DateField(blank=True)  # срок оплаты дата
    paid_fact = models.DateField(blank=True)  # факт оплаты дата
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)


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


class PretensionNote(models.Model):
    # СЗ на УПОБ об инициировании претензии
    number = models.CharField(max_length=10)
    note_date = models.DateField()
    penalty_amount = models.FloatField()
    letter_image = models.FileField(upload_to="pretension_note/%Y/%m/%d/%s")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    have_answer = models.BooleanField(default=False)
    answer_image = models.FileField(upload_to="pretension_note/answers/%Y/%m/%d/%s", blank=True)


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


class LawsuitNote(models.Model):
    # СЗ на ГД по исковой
    number = models.CharField(max_length=10)
    note_date = models.DateField()
    penalty_amount = models.FloatField()
    letter_image = models.FileField(upload_to="pretension_note/%Y/%m/%d/%s")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    have_answer = models.BooleanField(default=False)
    answer_image = models.FileField(upload_to="pretension_note/answers/%Y/%m/%d/%s", blank=True)

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
