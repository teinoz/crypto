from django.core.management.base import BaseCommand, CommandError
from crypto_app.models import Crypto, CoinValue
from binance.client import Client
import pandas as pd
from datetime import datetime, date, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import math
import json
import numpy as np
import random
from paho.mqtt import client as mqtt_client
import time

class Command(BaseCommand):
        print("Crypto Update")
        def handle(self, *args, **options):
            #BINANCE API
            api_key='kqgDcbokq1cNVvNd2yNwSGiVBFTSaeFDEa1xdRQmnW0wJ1xH6Mzhc4LoDtCuwUuA'
            api_secret='tgCrLfs3sQadf9WwQSnfXVXNjSCFPHhyGF13BQMhiZq6thnnoYnQA9mMlWEIiKSg'
            client = Client(api_key, api_secret)
            #MQTT SETUP
            broker = 'localhost'
            port = 1883
            topic = "/home/binance"
            client_id = f'python-mqtt-{random.randint(0, 1000)}'
            def connect_mqtt():
                def on_connect(client, userdata, flags, rc):
                    if rc == 0:
                        print("Connected to MQTT Broker!")
                    else:
                        print("Failed to connect, return code %d\n", rc)

                client = mqtt_client.Client(client_id)
                client.on_connect = on_connect
                client.connect(broker, port)
                return client
            def publish(client, binance_list, id_cryp):
                for el in binance_list:
                    time.sleep(0.5)
                    el.append(id_cryp)
                    msg = json.dumps(el)
                    result = client.publish(topic, msg)
                    status = result[0]
                    if status == 0:
                        print(f"Send `{msg}` to topic `{topic}`")
                    else:
                        print(f"Failed to send message to topic {topic}")
            aggiorna = {}
            crypto = Crypto.objects.all()
            crypto_list = list(crypto)
            print(crypto_list)
            for el in crypto_list:
                crypto_obj = Crypto.objects.get(id=el.id)
                valori = crypto_obj.values.last()
                #print(valori.open)
                crypto_symbol = str(el.symbol) + "USDT"
                dati_nuova_crypto = client.get_historical_klines(crypto_symbol, "1h", str(valori.close_time+1))
                if len(dati_nuova_crypto)>=2:
                    dati_nuova_crypto.pop()
                    cli = connect_mqtt()
                    publish(cli, dati_nuova_crypto, el.id)
"""
                    for el in dati_nuova_crypto:
                        up_data = CoinValue(open_time = int(el[0]), open = float(el[1]), close = float(el[2]), high = float(el[3]),  low = float(el[4]), volume=float(el[5]), close_time=int(el[6]), quote_asset_volume = float(el[7]), number_of_trades = int(el[8]), taker_buy_base_asset_volume = float(el[9]), taker_buy_quote_asset_volume = float(el[10]), crypto = crypto_obj)
                        up_data.save()
                        print(up_data)
"""
            dict_of_data = {}
            df = {}
            projection = 24
            col_names = ["open_time", "open", "high", "low", "close", "volume", "close_time", "number_of_trades"]
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
                X_close=np.array(df[crypto_df][['close']])
                X_open=np.array(df[crypto_df][['open']])

                #Remove last 24H since NaN
                X_close=X_close[:-projection]
                X_open=X_open[:-projection]
                #CREATE RESPONSE VECTORS FOR CLOSE AND OPEN
                Y_close=df[crypto_df]['prediction_close'].values
                Y_open=df[crypto_df]['prediction_open'].values

                Y_close=Y_close[:-projection]
                Y_open=Y_open[:-projection]

                #TRAIN / TEST SPLIT
                x_train_close, x_test_close, y_train_close, y_test_close = train_test_split(X_close,Y_close,test_size=.30)
                x_train_open, x_test_opne, y_train_open, y_test_open = train_test_split(X_open, Y_open, test_size=.30)

                #LINEAR REGRESSION CLOSE
                linReg_close=LinearRegression()
                linReg_close.fit(x_train_close,y_train_close)

                #LINEAR REGRESSION OPEN
                linReg_open=LinearRegression()
                linReg_open.fit(x_train_open, y_train_open)

                #PREDICTION FOR CLOSE
                x_projection_close= np.array(df[crypto_df][['close']])[-projection:]
                linReg_prediction_close=linReg_close.predict(x_projection_close)

                #PREDICITON FOR OPEN
                x_projection_open = np.array(df[crypto_df][['open']])[-projection:]
                linReg_prediction_open = linReg_open.predict(x_projection_open)

                print("Predicted 24h:", linReg_prediction_close[-1] , " Actual value now" , Y_close[-1])
                print("Predicted 1h:", linReg_prediction_close[0] , " Actual value now" , Y_close[-1])

                last_day = Crypto.objects.get(symbol=crypto_df).values.all().order_by('-id')[:24]
                last_day = list(reversed(last_day))
                id_value = [day.id for day in last_day]
                print(linReg_prediction_close)
                print(linReg_prediction_open)
                print(id_value)
                print(crypto_df)
                print(df[crypto_df].tail(25))
                for i in range(len(id_value)):
                    CoinValue.objects.filter(id=id_value[i]).update(prediction_close=linReg_prediction_close[i])
                    CoinValue.objects.filter(id=id_value[i]).update(prediction_open=linReg_prediction_open[i])
