# Generated by Django 4.1 on 2022-09-28 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0052_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]