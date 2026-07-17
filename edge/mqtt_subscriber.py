import json

import paho.mqtt.client as mqtt

from edge_processor import EdgeProcessor

processor = EdgeProcessor()


def on_connect(client, userdata, flags, reason_code, properties=None):

    print("Connected to MQTT Broker")

    client.subscribe("airport/raw/#")


def on_message(client, userdata, msg):

    payload = json.loads(msg.payload.decode())

    processor.process(payload)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect

client.on_message = on_message

client.connect("localhost", 1883)

client.loop_forever()