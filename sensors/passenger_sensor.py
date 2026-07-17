# import random
# import time
# from config import PASSENGER_INTERVAL, TOTAL_READINGS


# def generate_passenger_data():

#     for i in range(TOTAL_READINGS):

#         data = {
#             "sensor": "Passenger Counter",
#             "location": "Entrance A",
#             "passenger_count": random.randint(5, 50)
#         }

#         print(data)

#         time.sleep(PASSENGER_INTERVAL)


# if __name__ == "__main__":
#     generate_passenger_data()

import random

from base_sensor import BaseSensor
from config import RAW_PASSENGER_TOPIC, PASSENGER_INTERVAL


class PassengerSensor(BaseSensor):

    def __init__(self):
        super().__init__(RAW_PASSENGER_TOPIC, PASSENGER_INTERVAL)

    def generate_data(self):

        return {
            "sensor_id": "P001",
            "sensor_type": "Passenger Counter",
            "location": "Entrance A",
            "passenger_count": random.randint(10, 60)
        }


if __name__ == "__main__":
    sensor = PassengerSensor()
    sensor.run()