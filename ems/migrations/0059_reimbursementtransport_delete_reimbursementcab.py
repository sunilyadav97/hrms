# Generated by Django 4.1 on 2022-10-06 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0058_rename_vehcle_name_reimbursementcab_vehicle_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReimbursementTransport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transport_company', models.CharField(max_length=50)),
                ('vehicle_name', models.CharField(max_length=50)),
                ('vehicle_number', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
                ('date', models.DateField()),
                ('status', models.CharField(default='pending', max_length=50)),
                ('remark', models.CharField(blank=True, max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ems.employee')),
            ],
        ),
        migrations.DeleteModel(
            name='ReimbursementCab',
        ),
    ]
