import json
import threading

import paho.mqtt.client as mqtt

from django.utils.dateparse import parse_datetime

from airport.models import (
    PassengerData,
    QueueStatus,
    GateStatus,
    TemperatureLog,
    EmergencyAlert,
)


BROKER = "localhost"
PORT = 1883


# -------------------------------------------------
# Passenger Handler
# -------------------------------------------------

def save_passenger(payload):

    PassengerData.objects.create(
        sensor_id=payload["sensor_id"],
        location=payload["location"],
        passenger_count=payload["passenger_count"],
        passenger_flow=payload["passenger_flow"],
        edge_timestamp=parse_datetime(payload["edge_timestamp"]),
    )

    print("✅ Passenger Saved")


# -------------------------------------------------
# Queue Handler
# -------------------------------------------------

def save_queue(payload):

    queue_length = payload["queue_length"]

    if queue_length < 30:
        congestion = "LOW"
    elif queue_length < 70:
        congestion = "MEDIUM"
    else:
        congestion = "HIGH"

    QueueStatus.objects.create(
        area=payload["location"],
        queue_length=queue_length,
        waiting_time=payload["waiting_time"],
        congestion_level=congestion,
    )

    print("✅ Queue Saved")


# -------------------------------------------------
# Gate Handler
# -------------------------------------------------

def save_gate(payload):

    waiting = payload["passengers_waiting"]

    if waiting < 80:
        status = "AVAILABLE"
    elif waiting < 160:
        status = "BUSY"
    else:
        status = "FULL"

    GateStatus.objects.create(
        gate_name=payload["gate_name"],
        passengers_waiting=waiting,
        status=status,
    )

    print("✅ Gate Saved")


# -------------------------------------------------
# Temperature Handler
# -------------------------------------------------

def save_temperature(payload):

    TemperatureLog.objects.create(

        sensor_id=payload["sensor_id"],

        location=payload["location"],

        temperature=payload["temperature"]

    )

    print("✅ Temperature Saved")


# -------------------------------------------------
# Emergency Handler
# -------------------------------------------------

def save_emergency(payload):

    EmergencyAlert.objects.create(
        alert_type=payload["alert_type"],
        location=payload["location"],
        description=payload["description"],
        resolved=False,
    )

    print("✅ Emergency Saved")


# -------------------------------------------------
# MQTT Callbacks
# -------------------------------------------------

def on_connect(client, userdata, flags, reason_code, properties=None):

    print("✅ Django Connected")

    client.subscribe("airport/fog/#")


def on_message(client, userdata, msg):

    payload = json.loads(msg.payload.decode())

    print("\nReceived:")
    print(payload)

    sensor_type = payload.get("sensor_type")

    if sensor_type == "Passenger Counter":
        save_passenger(payload)

    elif sensor_type == "Queue Sensor":
        save_queue(payload)

    elif sensor_type == "Gate Sensor":
        save_gate(payload)

    elif sensor_type == "Temperature":
        save_temperature(payload)

    elif sensor_type == "Emergency":
        save_emergency(payload)

    else:
        print("Unknown Sensor Type:", sensor_type)


# -------------------------------------------------
# MQTT Client
# -------------------------------------------------

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message


def mqtt_loop():

    client.connect(BROKER, PORT)

    client.loop_forever()


def start():

    thread = threading.Thread(target=mqtt_loop, daemon=True)

    thread.start()