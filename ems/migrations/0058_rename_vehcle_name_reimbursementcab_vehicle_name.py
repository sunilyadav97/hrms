# Generated by Django 4.1 on 2022-10-04 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0057_reimbursementcab_remark'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reimbursementcab',
            old_name='vehcle_name',
            new_name='vehicle_name',
        ),
    ]