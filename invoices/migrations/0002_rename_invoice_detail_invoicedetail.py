# Generated by Django 4.2.10 on 2024-02-24 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Invoice_Detail',
            new_name='InvoiceDetail',
        ),
    ]
