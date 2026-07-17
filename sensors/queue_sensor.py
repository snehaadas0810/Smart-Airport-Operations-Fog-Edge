# import random
# import time
# from config import QUEUE_INTERVAL, TOTAL_READINGS


# def generate_queue_data():

#     for i in range(TOTAL_READINGS):

#         queue = random.randint(5, 120)

#         waiting = round(queue * 0.35, 2)

#         data = {
#             "sensor_id": "Q001",

#             "sensor_type": "Queue Sensor",

#             "location": "Security Check",

#             "queue_length": queue,

#             "waiting_time": waiting

#                 }

#         print(data)

#         time.sleep(QUEUE_INTERVAL)


# if __name__ == "__main__":
#     generate_queue_data()

import random

from base_sensor import BaseSensor
from config import RAW_QUEUE_TOPIC, QUEUE_INTERVAL


class QueueSensor(BaseSensor):

    def __init__(self):
        super().__init__(RAW_QUEUE_TOPIC, QUEUE_INTERVAL)

    def generate_data(self):

        queue = random.randint(5, 120)

        waiting = round(queue * 0.35, 2)

        return {
            "sensor_id": "Q001",
            "sensor_type": "Queue Sensor",
            "location": "Security Check",
            "queue_length": queue,
            "waiting_time": waiting
        }


if __name__ == "__main__":
    sensor = QueueSensor()
    sensor.run()