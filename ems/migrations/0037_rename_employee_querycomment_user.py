# Generated by Django 4.1 on 2022-09-13 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0036_alter_querycomment_employee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='querycomment',
            old_name='employee',
            new_name='user',
        ),
    ]
