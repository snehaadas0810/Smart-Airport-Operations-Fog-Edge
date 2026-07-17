import json

import paho.mqtt.client as mqtt

from fog_processor import FogProcessor

processor = FogProcessor()


def on_connect(client, userdata, flags, reason_code, properties=None):

    print("Fog Connected")

    client.subscribe("airport/edge/#")


def on_message(client, userdata, msg):

    payload = json.loads(msg.payload.decode())

    if "edge_timestamp" in payload:

        processor.process(payload)


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect

client.on_message = on_message

client.connect("localhost", 1883)

client.loop_forever()