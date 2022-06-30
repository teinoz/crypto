from django.shortcuts import render
from crypto_app.models import Crypto, CoinValue
from binance.client import Client
from django.http import HttpResponse
from io import BytesIO
import base64
import matplotlib.pyplot as plt
from crypto_app.forms import AddCrypto
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import json
from time import gmtime

# Create your views here.

@login_required
def new_crypto(request):
        #html = '<html><body>Request for %s.</body></html>' % symbol
        #return HttpResponse(html)
        api_key='kqgDcbokq1cNVvNd2yNwSGiVBFTSaeFDEa1xdRQmnW0wJ1xH6Mzhc4LoDtCuwUuA'
        api_secret='tgCrLfs3sQadf9WwQSnfXVXNjSCFPHhyGF13BQMhiZq6thnnoYnQA9mMlWEIiKSg'
        dbloader = []
        client = Client(api_key, api_secret)
        if request.method == 'POST':
            form = AddCrypto(request.POST)
            if form.is_valid():
                name = form.cleaned_data["name"]
                symbol = form.cleaned_data["symbol"]
                name = str(name)
                crypto_name = str(symbol)
                crypto_name = str(crypto_name).upper()
                crypto_symbol = crypto_name + "USDT"
                dati_nuova_crypto = client.get_historical_klines(crypto_symbol, "1h", 0)
                crypto = Crypto(name = name, symbol = crypto_name)
                crypto.save()
                dati_nuova_crypto.pop()
                for el in dati_nuova_crypto:
                    dbloader.append(CoinValue(open_time = int(el[0]), open = float(el[1]), close = float(el[2]), high = float(el[3]),  low = float(el[4]), volume=float(el[5]), close_time=int(el[6]), quote_asset_volume = float(el[7]), number_of_trades = int(el[8]), taker_buy_base_asset_volume = float(el[9]), taker_buy_quote_asset_volume = float(el[10]), crypto = crypto))
                CoinValue.objects.bulk_create(dbloader)
        html = "<h1>" + name + " added to the database</h1></br><a href='/'>Homepage</a>"
        return HttpResponse(html)

def show_crypto(request):
        tutte = {}
        #dt = datetime.now()
        ts = gmtime()
        ts_pred = datetime(ts.tm_year, ts.tm_mon, ts.tm_mday, ts.tm_hour+1, 0 , 0) - timedelta(days=1)
        ts_pred = int(datetime.timestamp(ts_pred)*1000)
        crypto_list = Crypto.objects.values()
        for el in crypto_list:
            valori = CoinValue.objects.filter(crypto_id=el["id"]).last()
            tutte[el["symbol"]] = {}
            tutte[el["symbol"]]["info"] = []
            tutte[el["symbol"]]["info"] = [el for el in crypto_list]
            tutte[el["symbol"]]["pred"] = "{:.2f}".format(valori.prediction_close)
            tutte[el["symbol"]]["var"] = "{:.2f}".format(((valori.prediction_close-valori.close)/valori.close)*100)
            prediction = CoinValue.objects.get(crypto_id=el["id"], open_time=ts_pred)
            tutte[el["symbol"]]["time"] = ts.tm_hour+1
            tutte[el["symbol"]]["pred_hour"] = "{:.2f}".format(prediction.prediction_close)
        all_cryp = {"tutte": tutte}
        return render(request, 'crypto_app/home.html', all_cryp)

@csrf_exempt
def graph(request):
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
            dati_nuova_crypto = client.get_historical_klines(crypto_symbol, Client.KLINE_INTERVAL_1MINUTE, "6 hour ago UTC")
            aggiorna[crypto_symbol] = []
            for dati in dati_nuova_crypto:
                tempo = int(dati[0])/1000
                tempo = str(datetime.fromtimestamp(tempo))
                tempo = tempo.split(".")[0].split(" ")[1]
                aggiorna[crypto_symbol].append([[int(t) for t in tempo.split(":")], float(dati[4])])
        print(aggiorna)
        return HttpResponse(json.dumps({'aggiorna': aggiorna}), content_type="application/json")
