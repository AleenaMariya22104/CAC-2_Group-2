# Generated by Django 4.2.9 on 2024-01-25 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electro', '0003_remove_customuser_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
