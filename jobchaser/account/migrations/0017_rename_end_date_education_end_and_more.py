# Generated by Django 4.2.7 on 2024-05-10 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_workexperience_end_date_workexperience_start_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='education',
            old_name='end_date',
            new_name='end',
        ),
        migrations.RenameField(
            model_name='education',
            old_name='institution',
            new_name='school',
        ),
        migrations.RenameField(
            model_name='education',
            old_name='specialization',
            new_name='specialisation',
        ),
        migrations.RenameField(
            model_name='education',
            old_name='start_date',
            new_name='start',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='date_of_birth',
            new_name='dob',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='educations',
            new_name='education',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='firstName',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='last_name',
            new_name='lastName',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='middle_name',
            new_name='middleName',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='month_of_experience',
            new_name='moe',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='skills',
            new_name='skill',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='workexperience',
            new_name='work',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='year_of_experience',
            new_name='yoe',
        ),
        migrations.RenameField(
            model_name='workexperience',
            old_name='still_work',
            new_name='current',
        ),
        migrations.RenameField(
            model_name='workexperience',
            old_name='end_date',
            new_name='end',
        ),
        migrations.RenameField(
            model_name='workexperience',
            old_name='start_date',
            new_name='start',
        ),
        migrations.RenameField(
            model_name='workexperience',
            old_name='top_skills',
            new_name='topSkill',
        ),
    ]
