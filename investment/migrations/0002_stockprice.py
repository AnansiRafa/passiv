# Generated by Django 4.2.20 on 2025-04-04 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('volume', models.BigIntegerField()),
                ('opportunity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_prices', to='investment.investmentopportunity')),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('opportunity', 'date')},
            },
        ),
    ]
