# Generated by Django 4.1 on 2022-08-27 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0012_rename_employeeattendance_attendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='intime',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='outtime',
            field=models.TimeField(blank=True),
        ),
    ]
