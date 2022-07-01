from django.core.management.base import BaseCommand, CommandError
from crypto_app.models import Crypto, CoinValue
import pandas as pd
from paho.mqtt import client as mqtt_client
import random
import time
import json

class Command(BaseCommand):
        print("Crypto Prediction")
        def handle(self, *args, **options):
            '''
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
            '''
            broker = 'localhost'
            port = 1883
            topic = "/home/binance"
            client_id = f'python-mqtt-{random.randint(0, 1000)}'
            lista = [12, 23, 12, 54]

            def connect_mqtt():
                def on_connect(client, userdata, flags, rc):
                    if rc == 0:
                        print("Connected to MQTT Broker!")
                    else:
                        print("Failed to connect, return code %d\n", rc)

                client = mqtt_client.Client(client_id)
                #client.username_pw_set(username, password)
                client.on_connect = on_connect
                client.connect(broker, port)
                return client

            def publish(client):
                msg_count = 0
                while True:
                    time.sleep(1)
                    msg = f"messages: {msg_count}"
                    msg = json.dumps(lista)
                    result = client.publish(topic, msg)
                    # result: [0, 1]
                    status = result[0]
                    if status == 0:
                        print(f"Send `{msg}` to topic `{topic}`")
                    else:
                        print(f"Failed to send message to topic {topic}")
                    msg_count += 1
            cli = connect_mqtt()
            publish(cli)
