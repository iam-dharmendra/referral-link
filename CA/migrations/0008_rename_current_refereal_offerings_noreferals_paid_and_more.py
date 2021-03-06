# Generated by Django 4.0.3 on 2022-04-08 04:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CA', '0007_offerings_current_refereal_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offerings',
            old_name='current_refereal',
            new_name='noReferals_paid',
        ),
        migrations.AlterField(
            model_name='casignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 23, 4, 22, 0, 874128)),
        ),
        migrations.AlterField(
            model_name='prsignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 23, 4, 22, 0, 873836)),
        ),
    ]
