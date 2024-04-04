from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Provider(models.Model):
    # Модель поставщика
    full_name = models.CharField(verbose_name='Полное наименование', max_length=200)
    cut_name = models.CharField(verbose_name='Сокращенное наименование', max_length=50)
    inn = models.IntegerField(verbose_name='ИНН', unique=True)
    sap_code = models.IntegerField(verbose_name='Код КА в SAP', unique=True)
    address = models.TextField('Адрес КА')
    e_mail = models.EmailField('Электронная почта КА')
    telephone = models.CharField(verbose_name='Телефон', max_length=20)
    penalty_for_supply = models.FloatField(verbose_name='Пеня за просрочку поставки', default=0.0)
    penalty_for_payment = models.FloatField(verbose_name='Пеня за просрочку оплаты', default=0.0)
    total_penalty = models.FloatField(verbose_name='Итого пеня', default=0.0)
    payd_penalty = models.FloatField(verbose_name='Оплаченные Пени', default=0.0)
    sum_of_pretensions = models.FloatField(verbose_name='Сумма выставленных претензий', default=0.0)

    class Meta:
        ordering = ['sap_code', '-total_penalty']
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'
    def __str__(self):
        return self.cut_name

    def get_sum_of_pretensions(self):
        # Возвращает сумму выставленных претензий
        pass

    def get_payd_penalty(self):
        # Возвращает оплаченную неустойку
        pass

    def get_total_penalty(self):
        #  Возвращает сумму неустойки по всем договорам
        all_contracts = self.contract_set.all()
        all_penalty = 0
        for contract in all_contracts:
            all_penalty += contract.make_contract_penalty()
        return all_penalty

    def get_penalty_for_payment(self):
        # Возвращает сумму неустойки за оплату
        all_contracts = self.contract_set.all()
        penalty_for_payment = 0
        for contract in all_contracts:
            contract.make_contract_penalty()
            penalty_for_payment += contract.penalty_for_payment
        return penalty_for_payment

    def get_penalty_for_supply(self):
        # Возвращает сумму неустойки за поставку
        all_contracts = self.contract_set.all()
        penalty_for_supply = 0
        for contract in all_contracts:
            contract.make_contract_penalty()
            penalty_for_supply += contract.penalty_for_supply
        return penalty_for_supply

    def get_contracts_count(self):
        # Возвращает количество догооров
        all_contracts = self.contract_set.all()
        return len(all_contracts)

    def get_bad_history(self):
        # Возвращает количество (или процент) договоров с просрочкой поставки
        all_contracts = self.contract_set.all()
        count = 0
        for contract in all_contracts:
            if contract.penalty_for_supply > 0:
                count += 1
        return count


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
    number = models.CharField(verbose_name='№ Договора', max_length=16, unique=True)
    start_date = models.DateField(verbose_name='Дата начала договора', blank=True)
    finish_date = models.DateField(verbose_name='Окончание договора', blank=True, null=True)  # Крайняя дата поставки
    contract_provider = models.ForeignKey(
        Provider,
        on_delete=models.PROTECT,
        verbose_name='Контрагент'
    )
    company = models.ForeignKey('Company', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Общество')  # Это общество группы с которым заключен договор
    employee = models.ForeignKey('Staff', on_delete=models.PROTECT, blank=True, verbose_name='Куратор договора')
    delivery_item = models.CharField(verbose_name='Предмет договора', max_length=200, blank=True)  # Предмет поставки
    amount = models.FloatField(verbose_name='Сумма договора')
    payment_term = models.IntegerField(verbose_name='Срок оплаты, дней', null=True, default=60)
    deliver_penalty_percent = models.FloatField(verbose_name='Процент пени за просрочку поставки', blank=True, null=True)
    max_deliver_penalty_percent = models.FloatField(verbose_name='Максимум пени за просрочку поставки', blank=True, null=True)
    paid_penalty_percent = models.FloatField(verbose_name='Процент пени за просрочку поставки', blank=True, null=True)
    max_paid_penalty_percent = models.FloatField(verbose_name='Максимум пени за просрочку поставки', blank=True, null=True)
    already_get_amount = models.FloatField(verbose_name='Уже поставлено', default=0.0)  # Сумма поставленного
    remains_deliver_amount = models.FloatField(verbose_name='Остаток к поставке', blank=True)
    penalty_for_supply = models.FloatField(verbose_name='Сумма пени за просрочку поставки', default=0.0)
    penalty_for_payment = models.FloatField(verbose_name='Сумма пени за просрочку оплаты', default=0.0)
    sum_of_pretensions = models.FloatField(verbose_name='Суммарная пеня по договору', default=0.0)
    pretension_status = models.CharField(
        verbose_name='Статус претензионной работы',
        max_length=2,
        choices=PRETENSION_CHOICES,
        default=UNINITIATED
    )
    paid_penalty = models.FloatField(verbose_name='Оплачено пени со стороны КА', default=0.0)
    is_done = models.BooleanField(verbose_name='Договор закрыт', default=False)

    class Meta:
        ordering = ['start_date', '-sum_of_pretensions']
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'

    def __str__(self):
        return f'Договор {self.number} от {self.start_date} на сумму {self.amount} р, сумма пени {self.sum_of_pretensions}'

    # def save(self, *args, **kwargs):
    #     self.remains_deliver_amount = self.amount
    #     super(Contract, self).save(*args, **kwargs)

    def make_already_get_amount(self):
        #  Расчитывает сумму поставленного и изменяет значение остатка к поставке
        already_amount = 0
        all_delivers = self.deliver_set.all()
        if all_delivers:
            for deliver in all_delivers:
                already_amount += deliver.total
            self.already_get_amount = already_amount
            self.remains_deliver_amount = self.amount - already_amount
            self.save()

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
        self.save()
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
    full_name = models.CharField(verbose_name='Полное наименование', max_length=200)
    cut_name = models.CharField(verbose_name='Сокращенное наименование', max_length=50)
    inn = models.IntegerField(verbose_name='ИНН', unique=True)
    sap_code = models.IntegerField(verbose_name='Код в системе SAP', unique=True)
    address = models.TextField(verbose_name='Адрес')
    e_mail = models.EmailField(verbose_name='Электронная почта')
    telephone = models.CharField(verbose_name='№ Телефона', max_length=20)

    class Meta:
        ordering = ['cut_name']
        verbose_name = 'Общество'
        verbose_name_plural = 'Общества'

    def __str__(self):
        return self.cut_name


class Department(models.Model):
    # Отдел
    title = models.CharField(verbose_name='Наименование отдела', max_length=72)
    cut = models.CharField(verbose_name='Сокращенное наименование', max_length=10)

    class Meta:
        ordering = ['cut']
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.title


class Staff(models.Model):
    # Персонал
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    sap_id = models.IntegerField(verbose_name='Код в системе SAP', unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name='Отдел')
    dep_director = models.BooleanField(verbose_name='Статус начальника отдела', default=False)
    main_man = models.BooleanField(verbose_name='Статус руководителя верхнего звена', default=False)

    class Meta:
        ordering = ['main_man', 'dep_director', 'sap_id']
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.user.username


class Deliver(models.Model):
    # Поставка товара на сумму по договору
    invoice = models.CharField(verbose_name='№ Счета-фактуры/УПД', max_length=128)  # № счет-фактуры (УПД)
    invoice_date = models.DateField(verbose_name='Дата фактуры/УПД')  # Дата фактуры
    total = models.FloatField(verbose_name='Сумма поставки', )  #Сумма фактуры
    delivered = models.DateField(verbose_name='Дата поставки', blank=True, null=True)
    payment_term = models.DateField(verbose_name='Дата оплаты', blank=True, null=True)  # срок оплаты дата
    paid_fact = models.DateField(verbose_name='Факт оплаты', blank=True, null=True)  # факт оплаты дата
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name='Договор')

    class Meta:
        ordering = ['invoice_date', 'invoice']
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'

    def __str__(self):
        return f'Поставка {self.invoice} от {self.invoice_date}  сумма {self.total} по договору {self.contract.number}'

    def set_payment_term(self):
        # Установить срок оплаты
        pass


class BeforePretension(models.Model):
    # Допретензионное требование
    number = models.CharField(verbose_name='№ Допретензионного требования', max_length=10)
    note_date = models.DateField(verbose_name='Дата')
    penalty_amount = models.FloatField(verbose_name='Сумма требований')
    letter_image = models.FileField(verbose_name='Письмо (скан)', upload_to="beforepretension/%Y/%m/%d/%s")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name='Договор')
    have_answer = models.BooleanField(verbose_name='Статус ответа', default=False)
    answer_image = models.FileField(verbose_name='Ответ (скан)', upload_to="beforepretension/answers/%Y/%m/%d/%s", blank=True)
    is_satisfied = models.BooleanField(verbose_name='Статус удовлетворения требований', default=False)
    penalty_paid = models.FloatField(verbose_name='Сумма оплаты', default=0)

    class Meta:
        ordering = ['note_date']
        verbose_name = 'Допретензионное требование'
        verbose_name_plural = 'Допретензионные требования'

    def __str__(self):
        return f'№ {self.number} от {self.note_date}'


class PretensionNote(models.Model):
    # СЗ на УПОБ об инициировании претензии
    number = models.CharField(verbose_name='№ служебки на УПОБ', max_length=10)
    note_date = models.DateField(verbose_name='Дата СЗ')
    penalty_amount = models.FloatField(verbose_name='Сумма требований')
    letter_image = models.FileField(verbose_name='Служебная записка (скан)', upload_to="pretension_note/%Y/%m/%d/%s")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name='Договор')
    have_answer = models.BooleanField(verbose_name='Статус ответа', default=False)
    answer_image = models.FileField(verbose_name='Ответ (скан)', upload_to="pretension_note/answers/%Y/%m/%d/%s", blank=True)

    class Meta:
        ordering = ['note_date']
        verbose_name = 'СЗ об инициировании ПИР'
        verbose_name_plural = 'СЗ об инициировании ПИР'

    def __str__(self):
        return f'№ {self.number} от {self.note_date}'


class Pretension(models.Model):
    # Претензия
    number = models.CharField(verbose_name='№ Претензии', max_length=10)
    note_date = models.DateField(verbose_name='Дата претензии')
    penalty_amount = models.FloatField(verbose_name='Сумма требований')
    letter_image = models.FileField(verbose_name='Претензия (скан)', upload_to="pretension/%Y/%m/%d/%s")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name='Договор')
    have_answer = models.BooleanField(verbose_name='Признак ответа', default=False)
    answer_image = models.FileField(verbose_name='Ответ (скан)', upload_to="pretension/answers/%Y/%m/%d/%s", blank=True)
    is_satisfied = models.BooleanField(verbose_name='Признак оплаты', default=False)
    penalty_paid = models.FloatField(verbose_name='Сумма оплаты', default=0)

    class Meta:
        ordering = ['note_date']
        verbose_name = 'Претензия'
        verbose_name_plural = 'Претензии'

    def __str__(self):
        return f'№ {self.number} от {self.note_date}'


class LawsuitNote(models.Model):
    # СЗ на ГД по исковой
    number = models.CharField(verbose_name='№ СЗ на ГД об инициировании ИР', max_length=10)
    note_date = models.DateField(verbose_name='Дата СЗ')
    penalty_amount = models.FloatField(verbose_name='Сумма требований')
    letter_image = models.FileField(verbose_name='СЗ (скан)', upload_to="pretension_note/%Y/%m/%d/%s")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name='Договор')
    have_answer = models.BooleanField(verbose_name='Признак ответа', default=False)
    answer_image = models.FileField(verbose_name='Ответ (скан)', upload_to="pretension_note/answers/%Y/%m/%d/%s", blank=True)

    class Meta:
        ordering = ['note_date']
        verbose_name = 'СЗ об инициировании исковой'
        verbose_name_plural = 'СЗ об инициировании исковой'

    def __str__(self):
        return f'№ {self.number} от {self.note_date}'


class Lawsuit(models.Model):
    # Иск в суд
    number = models.CharField(verbose_name='№ Искового заявления', max_length=10)
    note_date = models.DateField(verbose_name='Дата искового')
    penalty_amount = models.FloatField(verbose_name='Сумма требований')
    letter_image = models.FileField(verbose_name='Исковое (скан)', upload_to="lawsuit/%Y/%m/%d/%s")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name='Договор')
    case = models.CharField(verbose_name='№ Дела', max_length=100, blank=True)
    decision_image = models.FileField(verbose_name='Решение суда (скан)', upload_to="lawsuit/decision/%Y/%m/%d/%s", blank=True)
    decision_penalty = models.FloatField(verbose_name='Сумма по решению суда', blank=True)
    is_satisfied = models.BooleanField(verbose_name='Признак оплаты КА', default=False)
    penalty_paid = models.FloatField(verbose_name='Сумма оплаты', default=0)

    class Meta:
        ordering = ['note_date']
        verbose_name = 'Исковое требование'
        verbose_name_plural = 'Исковые требования'

    def __str__(self):
        return f'№ {self.number} от {self.note_date}'
