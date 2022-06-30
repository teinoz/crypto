from django.core.management.base import BaseCommand, CommandError
from crypto_app.models import Crypto, CoinValue
import pandas as pd

class Command(BaseCommand):
        print("Crypto Prediction")
        def handle(self, *args, **options):
            dict_of_data = {}
            df = {}
            projection = 1
            col_names = ["open_time", "open", "high", "low", "close", "volume", "close_time", "number_of_trades"]
            crypto = Crypto.objects.all()
            crypto_list = list(crypto)
            print(crypto_list)
            for el in crypto_list:
                crypto_obj = Crypto.objects.get(id=el.id)
                valori = crypto_obj.values.all()
                crypto_symbol = str(el.symbol) + "USDT"
                #print(el.symbol)
                dict_of_data[el.symbol] = []
                for dati in valori:
                    dict_of_data[el.symbol].append([dati.open_time, dati.open, dati.high, dati.low, dati.close, dati.volume, dati.close_time, dati.number_of_trades])
                df[el.symbol] = pd.DataFrame(dict_of_data[el.symbol], columns=col_names)
                df[el.symbol]["prediction_close"]=df[el.symbol][["close"]].shift(-projection)
                df[el.symbol]["prediction_open"]=df[el.symbol][["open"]].shift(-projection)
            for crypto_df in df:
                print(crypto_df)
                print(df[crypto_df])
