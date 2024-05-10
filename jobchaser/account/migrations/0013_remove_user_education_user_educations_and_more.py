# Generated by Django 4.2.7 on 2024-05-09 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_education_user_education'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='education',
        ),
        migrations.AddField(
            model_name='user',
            name='educations',
            field=models.ManyToManyField(related_name='users', to='account.education'),
        ),
        migrations.AlterField(
            model_name='education',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_educations', to=settings.AUTH_USER_MODEL),
        ),
    ]
