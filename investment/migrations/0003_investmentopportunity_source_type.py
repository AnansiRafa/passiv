# Generated by Django 4.2.20 on 2025-04-04 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0002_stockprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmentopportunity',
            name='source_type',
            field=models.CharField(choices=[('stock', 'Stock'), ('crypto', 'Crypto')], default='stock', max_length=10),
        ),
    ]
