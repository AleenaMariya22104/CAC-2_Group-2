# Generated by Django 4.2.9 on 2024-01-27 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('electro', '0016_unit_invoiced_unit_status_invoice_unit_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='generated_invoices', to=settings.AUTH_USER_MODEL),
        ),
    ]
