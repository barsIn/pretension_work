# Generated by Django 5.0.2 on 2024-02-27 16:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('cut_name', models.CharField(max_length=50)),
                ('inn', models.IntegerField()),
                ('sap_code', models.IntegerField()),
                ('address', models.TextField()),
                ('e_mail', models.EmailField(max_length=254)),
                ('telephone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=72)),
                ('cut', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('cut_name', models.CharField(max_length=50)),
                ('inn', models.IntegerField()),
                ('sap_code', models.IntegerField()),
                ('address', models.TextField()),
                ('e_mail', models.EmailField(max_length=254)),
                ('telephone', models.CharField(max_length=20)),
                ('penalty_for_supply', models.FloatField(default=0.0)),
                ('penalty_for_payment', models.FloatField(default=0.0)),
                ('total_penalty', models.FloatField(default=0.0)),
                ('payd_penalty', models.FloatField(default=0.0)),
                ('sum_of_pretensions', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=9)),
                ('start_date', models.DateField(blank=True)),
                ('finish_date', models.DateField(blank=True)),
                ('delivery_item', models.CharField(blank=True, max_length=200)),
                ('amount', models.FloatField(blank=True)),
                ('payment_term', models.IntegerField()),
                ('deliver_penalty_percent', models.FloatField(blank=True)),
                ('max_deliver_penalty_percent', models.FloatField(blank=True)),
                ('paid_penalty_percent', models.FloatField(blank=True)),
                ('max_paid_penalty_percent', models.FloatField(blank=True)),
                ('already_get_amount', models.FloatField(default=0.0)),
                ('remains_deliver_amount', models.FloatField(blank=True, default=models.FloatField(blank=True))),
                ('penalty_for_supply', models.FloatField(default=0.0)),
                ('penalty_for_payment', models.FloatField(default=0.0)),
                ('sum_of_pretensions', models.FloatField(default=0.0)),
                ('pretension_status', models.CharField(choices=[('UI', 'Не инициирована'), ('BP', 'Допретензионное направлено'), ('PN', 'Направлена СЗ на претензию'), ('PT', 'Направлена претензия'), ('LN', 'Направлена СЗ по исковому'), ('LS', 'Иск подан в суд'), ('LF', 'Суд завершен'), ('SM', 'Прекращено руководством'), ('FN', 'Завершена')], default='UI', max_length=2)),
                ('paid_penalty', models.FloatField(default=0.0)),
                ('is_done', models.BooleanField(default=False)),
                ('company', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='contracts.company')),
                ('contract_provider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contracts.provider')),
            ],
        ),
        migrations.CreateModel(
            name='BeforePretension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('note_date', models.DateField()),
                ('penalty_amount', models.FloatField()),
                ('letter_image', models.FileField(upload_to='beforepretension/%Y/%m/%d/%s')),
                ('have_answer', models.BooleanField(default=False)),
                ('answer_image', models.FileField(blank=True, upload_to='beforepretension/answers/%Y/%m/%d/%s')),
                ('is_satisfied', models.BooleanField(default=False)),
                ('penalty_paid', models.FloatField(default=0)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contract')),
            ],
        ),
        migrations.CreateModel(
            name='Deliver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice', models.CharField(max_length=128)),
                ('invoice_date', models.DateField()),
                ('total', models.FloatField()),
                ('delivered', models.DateField(blank=True)),
                ('payment_term', models.DateField(blank=True)),
                ('paid_fact', models.DateField(blank=True)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contract')),
            ],
        ),
        migrations.CreateModel(
            name='Lawsuit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('note_date', models.DateField()),
                ('penalty_amount', models.FloatField()),
                ('letter_image', models.FileField(upload_to='lawsuit/%Y/%m/%d/%s')),
                ('case', models.CharField(blank=True, max_length=100)),
                ('decision_image', models.FileField(blank=True, upload_to='lawsuit/decision/%Y/%m/%d/%s')),
                ('decision_penalty', models.FloatField(blank=True)),
                ('is_satisfied', models.BooleanField(default=False)),
                ('penalty_paid', models.FloatField(default=0)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contract')),
            ],
        ),
        migrations.CreateModel(
            name='LawsuitNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('note_date', models.DateField()),
                ('penalty_amount', models.FloatField()),
                ('letter_image', models.FileField(upload_to='pretension_note/%Y/%m/%d/%s')),
                ('have_answer', models.BooleanField(default=False)),
                ('answer_image', models.FileField(blank=True, upload_to='pretension_note/answers/%Y/%m/%d/%s')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contract')),
            ],
        ),
        migrations.CreateModel(
            name='Pretension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('note_date', models.DateField()),
                ('penalty_amount', models.FloatField()),
                ('letter_image', models.FileField(upload_to='pretension/%Y/%m/%d/%s')),
                ('have_answer', models.BooleanField(default=False)),
                ('answer_image', models.FileField(blank=True, upload_to='pretension/answers/%Y/%m/%d/%s')),
                ('is_satisfied', models.BooleanField(default=False)),
                ('penalty_paid', models.FloatField(default=0)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contract')),
            ],
        ),
        migrations.CreateModel(
            name='PretensionNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('note_date', models.DateField()),
                ('penalty_amount', models.FloatField()),
                ('letter_image', models.FileField(upload_to='pretension_note/%Y/%m/%d/%s')),
                ('have_answer', models.BooleanField(default=False)),
                ('answer_image', models.FileField(blank=True, upload_to='pretension_note/answers/%Y/%m/%d/%s')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contract')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sap_id', models.IntegerField()),
                ('dep_director', models.BooleanField(default=False)),
                ('main_man', models.BooleanField(default=False)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contracts.department')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='contract',
            name='employee',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='contracts.staff'),
        ),
    ]
