import time

from mqtt_client import MQTTClient


class BaseSensor:

    def __init__(self, topic, interval):

        self.topic = topic

        self.interval = interval

        self.client = MQTTClient()

    def generate_data(self):
        """
        Child classes must implement this method.
        """
        raise NotImplementedError

    def run(self):

        while True:

            data = self.generate_data()

            self.client.publish(self.topic, data)

            time.sleep(self.interval)