# Generated by Django 4.1 on 2022-08-31 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0017_alter_leave_no_of_leaves'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave',
            name='no_of_leaves',
        ),
    ]
