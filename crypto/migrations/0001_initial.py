# Generated by Django 4.2.20 on 2025-04-04 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coingecko_id', models.CharField(max_length=100, unique=True)),
                ('symbol', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('image', models.URLField(blank=True, null=True)),
                ('market_cap_rank', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CryptoPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_usd', models.DecimalField(decimal_places=10, max_digits=20)),
                ('market_cap', models.BigIntegerField(blank=True, null=True)),
                ('volume_24h', models.BigIntegerField(blank=True, null=True)),
                ('fetched_at', models.DateTimeField(auto_now_add=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='crypto.cryptoasset')),
            ],
            options={
                'ordering': ['-fetched_at'],
            },
        ),
    ]
