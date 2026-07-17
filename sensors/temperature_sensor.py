import random

from base_sensor import BaseSensor
from config import RAW_TEMPERATURE_TOPIC, TEMPERATURE_INTERVAL


class TemperatureSensor(BaseSensor):

    def __init__(self):
        super().__init__(RAW_TEMPERATURE_TOPIC, TEMPERATURE_INTERVAL)

    def generate_data(self):

        return {

            "sensor_id": "T001",

            "sensor_type": "Temperature",

            "location": "Terminal 1",

            "temperature": round(random.uniform(18, 30), 2)

        }


if __name__ == "__main__":

    sensor = TemperatureSensor()

    sensor.run()