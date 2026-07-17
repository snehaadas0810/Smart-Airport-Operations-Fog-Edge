# from datetime import datetime

# from validator import validate_message
# from logger import log_message


# class EdgeProcessor:

#     def process(self, data):

#         if not validate_message(data):
#             print("Invalid Data")

#             return

#         data["edge_timestamp"] = datetime.now().isoformat()

#         log_message(data)

#         print("Forwarding to Fog Layer...\n")

#         return data


from datetime import datetime

from validator import validate_message
from logger import log_message
from publisher import EdgePublisher


class EdgeProcessor:

    def __init__(self):

        self.publisher=EdgePublisher()

    def process(self,data):

        if not validate_message(data):

            return

        data["edge_timestamp"]=datetime.now().isoformat()

        log_message(data)

        sensor=data["sensor_type"]

        topic_map={

            "Passenger Counter":"airport/edge/passenger",

            "Queue Sensor":"airport/edge/queue",

            "Gate Sensor":"airport/edge/gate",

            "Temperature":"airport/edge/temperature",

            "Emergency":"airport/edge/emergency"

        }

        topic=topic_map.get(sensor)

        if topic:

            self.publisher.publish(topic,data)