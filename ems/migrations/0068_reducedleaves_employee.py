# Generated by Django 4.1 on 2022-10-09 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0067_reducedleaves_is_late'),
    ]

    operations = [
        migrations.AddField(
            model_name='reducedleaves',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ems.employee'),
        ),
    ]