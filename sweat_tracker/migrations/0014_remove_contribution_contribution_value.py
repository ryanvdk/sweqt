# Generated by Django 5.2.1 on 2025-06-04 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sweat_tracker', '0013_rename_work_units_contribution_units_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contribution',
            name='contribution_value',
        ),
    ]
