import random

from base_sensor import BaseSensor
from config import RAW_GATE_TOPIC, GATE_INTERVAL


GATES = [

    "A1",

    "A2",

    "B1",

    "B2"

]


class GateSensor(BaseSensor):

    def __init__(self):

        super().__init__(RAW_GATE_TOPIC, GATE_INTERVAL)

    def generate_data(self):

        return {

            "sensor_id": "G001",

            "sensor_type": "Gate Sensor",

            "gate_name": random.choice(GATES),

            "passengers_waiting": random.randint(20, 250)

        }


if __name__ == "__main__":

    sensor = GateSensor()

    sensor.run()