# Generated by Django 4.0.3 on 2022-04-06 10:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CA', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='casignup',
            name='subuser',
        ),
        migrations.AlterField(
            model_name='casignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 21, 10, 14, 3, 724459)),
        ),
        migrations.AlterField(
            model_name='prsignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 21, 10, 14, 3, 724020)),
        ),
    ]
