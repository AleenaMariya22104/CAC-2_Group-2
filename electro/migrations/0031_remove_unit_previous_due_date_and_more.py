# Generated by Django 4.2.7 on 2024-01-29 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('electro', '0030_unit_previous_due_date_unit_previous_units_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unit',
            name='previous_due_date',
        ),
        migrations.RemoveField(
            model_name='unit',
            name='previous_units',
        ),
        migrations.RemoveField(
            model_name='unit',
            name='timestamp',
        ),
    ]
