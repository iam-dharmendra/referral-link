# Generated by Django 4.0.3 on 2022-04-06 12:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CA', '0003_rename_tier1_offerings_percentage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 21, 12, 27, 32, 38646)),
        ),
        migrations.AlterField(
            model_name='prsignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 21, 12, 27, 32, 38181)),
        ),
    ]