import threading

from passenger_sensor import PassengerSensor
from queue_sensor import QueueSensor
from gate_sensor import GateSensor
from temperature_sensor import TemperatureSensor
from emergency_sensor import EmergencySensor


def run_sensor(sensor):
    sensor.run()


def main():
    sensors = [
        PassengerSensor(),
        QueueSensor(),
        GateSensor(),
        TemperatureSensor(),
        EmergencySensor(),
    ]

    threads = []

    for sensor in sensors:
        thread = threading.Thread(target=run_sensor, args=(sensor,))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    print("✅ All sensors started successfully...")

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
