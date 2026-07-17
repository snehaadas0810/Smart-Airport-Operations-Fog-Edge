import json
import paho.mqtt.client as mqtt

from config import BROKER, PORT


class MQTTClient:

    def __init__(self):

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        self.client.connect(BROKER, PORT)

    def publish(self, topic, data):

        payload = json.dumps(data)

        self.client.publish(topic, payload)

        print(f"Published -> {topic}: {payload}")