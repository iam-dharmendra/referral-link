# Generated by Django 4.0.3 on 2022-04-08 05:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CA', '0009_alter_casignup_payment_due_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 23, 5, 5, 57, 51015)),
        ),
        migrations.AlterField(
            model_name='offerings',
            name='monthlyAmount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='offerings',
            name='pendingAmount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='offerings',
            name='totalAmount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='prsignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 23, 5, 5, 57, 50340)),
        ),
    ]
