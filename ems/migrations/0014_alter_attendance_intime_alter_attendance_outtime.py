# Generated by Django 4.1 on 2022-08-27 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0013_alter_attendance_intime_alter_attendance_outtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='intime',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='outtime',
            field=models.TimeField(blank=True, null=True),
        ),
    ]