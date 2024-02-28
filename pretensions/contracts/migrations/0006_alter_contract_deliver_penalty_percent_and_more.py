# Generated by Django 5.0.2 on 2024-02-28 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0005_alter_contract_deliver_penalty_percent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='deliver_penalty_percent',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='max_deliver_penalty_percent',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='max_paid_penalty_percent',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='number',
            field=models.CharField(max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='paid_penalty_percent',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='deliver',
            name='delivered',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='deliver',
            name='payment_term',
            field=models.DateField(blank=True, null=True),
        ),
    ]