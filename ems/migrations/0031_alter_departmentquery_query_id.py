# Generated by Django 4.1 on 2022-09-12 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0030_departmentquery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departmentquery',
            name='query_id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
    ]