# Generated by Django 4.2.9 on 2024-01-26 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electro', '0011_remove_unit_user_unit_customer_unit_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='units',
            field=models.IntegerField(default=0),
        ),
    ]
