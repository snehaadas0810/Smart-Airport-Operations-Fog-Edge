import threading

from passenger_sensor import generate_passenger_data
from queue_sensor import generate_queue_data
from gate_sensor import generate_gate_data
from temperature_sensor import generate_temperature
from emergency_sensor import generate_emergency


threads = [
    threading.Thread(target=generate_passenger_data),
    threading.Thread(target=generate_queue_data),
    threading.Thread(target=generate_gate_data),
    threading.Thread(target=generate_temperature),
    threading.Thread(target=generate_emergency),
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()