# Generated by Django 4.2.11 on 2024-04-23 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_attendance_leaverequest_remove_book_authors_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.employee'),
        ),
        migrations.AlterField(
            model_name='leaverequest',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.employee'),
        ),
    ]
