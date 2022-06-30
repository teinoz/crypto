# Generated by Django 4.0.4 on 2022-06-22 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crypto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('symbol', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='CoinValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_time', models.IntegerField()),
                ('close_time', models.IntegerField()),
                ('open', models.FloatField()),
                ('close', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('volume', models.FloatField()),
                ('quote_asset_volume', models.FloatField()),
                ('number_of_trades', models.IntegerField()),
                ('taker_buy_base_asset_volume', models.FloatField()),
                ('taker_buy_quote_asset_volume', models.FloatField()),
                ('crypto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='crypto_app.crypto')),
            ],
        ),
    ]
