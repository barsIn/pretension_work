# Generated by Django 5.0.2 on 2024-02-28 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0003_alter_contract_finish_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='payment_term',
            field=models.IntegerField(blank=True, default=60),
        ),
    ]
