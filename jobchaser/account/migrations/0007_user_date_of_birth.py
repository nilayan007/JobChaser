# Generated by Django 4.2.7 on 2024-05-08 11:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_user_middle_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default=datetime.date(1900, 1, 1)),
        ),
    ]