from django.db import models

# Create your models here.

class Crypto(models.Model):
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=10, unique = True)

    def __str__(self):
        return self.symbol


class CoinValue(models.Model):
    crypto = models.ForeignKey(Crypto,related_name='values', on_delete=models.CASCADE)
    open_time = models.IntegerField()
    close_time = models.IntegerField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.FloatField()
    quote_asset_volume = models.FloatField()
    number_of_trades = models.IntegerField()
    taker_buy_base_asset_volume = models.FloatField()
    taker_buy_quote_asset_volume = models.FloatField()
    prediction_open = models.FloatField(default=0)
    prediction_close = models.FloatField(default=0)
