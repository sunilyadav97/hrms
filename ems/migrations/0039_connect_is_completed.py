# Generated by Django 4.1 on 2022-09-14 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0038_connect'),
    ]

    operations = [
        migrations.AddField(
            model_name='connect',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
