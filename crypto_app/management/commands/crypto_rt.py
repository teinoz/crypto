from django.core.management.base import BaseCommand, CommandError
from crypto_app.models import Crypto, CoinValue
from binance.client import Client
from datetime import datetime, timedelta

class Command(BaseCommand):
        print("test")
        def handle(self, *args, **options):
            api_key='kqgDcbokq1cNVvNd2yNwSGiVBFTSaeFDEa1xdRQmnW0wJ1xH6Mzhc4LoDtCuwUuA'
            api_secret='tgCrLfs3sQadf9WwQSnfXVXNjSCFPHhyGF13BQMhiZq6thnnoYnQA9mMlWEIiKSg'
            client = Client(api_key, api_secret)
            aggiorna = {}
            crypto = Crypto.objects.all()
            crypto_list = list(crypto)
            print(crypto_list)
            for el in crypto_list:
                crypto_symbol = str(el.symbol) + "USDT"
                last_hour_date_time = datetime.now() - timedelta(hours = 1)
                raw_time = datetime.timestamp(last_hour_date_time)
                fixed_time = int(str(raw_time).split(".")[0])*1000000
                print(fixed_time)
                dati_nuova_crypto = client.get_historical_klines(crypto_symbol, Client.KLINE_INTERVAL_1MINUTE, "1 hour ago UTC")
                print(dati_nuova_crypto)
                aggiorna[crypto_symbol] = []
                for dati in dati_nuova_crypto:
                    aggiorna[crypto_symbol].append([dati[0], dati[4]])
            print(aggiorna)
            return HttpResponse(json.dumps({'aggiorna': aggiorna}), content_type="application/json")
