# Generated by Django 4.2.11 on 2024-04-17 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_alter_employee_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='is_active',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
