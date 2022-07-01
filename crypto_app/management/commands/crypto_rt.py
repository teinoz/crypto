from django.core.management.base import BaseCommand, CommandError
from crypto_app.models import Crypto, CoinValue
from binance.client import Client
from datetime import datetime, timedelta
import random
from paho.mqtt import client as mqtt_client
import json

class Command(BaseCommand):
        print("Reciver")
        def handle(self, *args, **options):
            broker = 'localhost'
            port = 1883
            topic = "/home/binance"
            client_id = f'python-mqtt-{random.randint(0, 100)}'
            lista = [12, 23, 12, 54]

            def connect_mqtt() -> mqtt_client:
                def on_connect(client, userdata, flags, rc):
                    if rc == 0:
                        print("Connected to MQTT Broker!")
                    else:
                        print("Failed to connect, return code %d\n", rc)

                client = mqtt_client.Client(client_id)
                client.on_connect = on_connect
                client.connect(broker, port)
                return client

            def subscribe(client: mqtt_client):
                def on_message(client, userdata, msg):
                    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
                    el = json.loads(msg.payload.decode())
                    crypto_obj = Crypto.objects.get(id = el[-1])
                    up_data = CoinValue(open_time = int(el[0]), open = float(el[1]), close = float(el[2]), high = float(el[3]),  low = float(el[4]), volume=float(el[5]), close_time=int(el[6]), quote_asset_volume = float(el[7]), number_of_trades = int(el[8]), taker_buy_base_asset_volume = float(el[9]), taker_buy_quote_asset_volume = float(el[10]), crypto = crypto_obj)
                    up_data.save()
                    print(up_data)
                client.subscribe(topic)
                client.on_message = on_message


            def run():
                client = connect_mqtt()
                subscribe(client)
                client.loop_forever()


            run()
