# Generated by Django 4.1 on 2022-09-03 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0021_alter_employee_avtar'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
