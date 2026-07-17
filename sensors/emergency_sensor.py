import random

from base_sensor import BaseSensor
from config import RAW_EMERGENCY_TOPIC, EMERGENCY_INTERVAL


EVENTS = [

    "Fire",

    "Medical",

    "Security",

    "Smoke"

]


class EmergencySensor(BaseSensor):

    def __init__(self):

        super().__init__(RAW_EMERGENCY_TOPIC, EMERGENCY_INTERVAL)

    def generate_data(self):

        event = random.choice(EVENTS)

        return {

            "sensor_id": "E001",

            "sensor_type": "Emergency",

            "alert_type": event.upper(),

            "location": "Terminal 2",

            "description": f"{event} detected"

        }


if __name__ == "__main__":

    sensor = EmergencySensor()

    sensor.run()