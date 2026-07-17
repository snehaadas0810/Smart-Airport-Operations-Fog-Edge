import json
import paho.mqtt.client as mqtt


class EdgePublisher:

    def __init__(self):

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        self.client.connect("localhost",1883)

    def publish(self,topic,data):

        payload=json.dumps(data)

        self.client.publish(topic,payload)

        print(f"Published -> {topic}")