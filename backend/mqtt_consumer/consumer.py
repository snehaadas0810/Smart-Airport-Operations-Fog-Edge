import json
import threading
import logging

import paho.mqtt.client as mqtt

from dashboard.tasks import save_sensor_data


# -------------------------------------------------
# Configuration
# -------------------------------------------------

BROKER = "localhost"
PORT = 1883
TOPIC = "airport/fog/#"


# -------------------------------------------------
# Logger
# -------------------------------------------------

logger = logging.getLogger(__name__)


# -------------------------------------------------
# MQTT Callbacks
# -------------------------------------------------

def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        logger.info("✅ MQTT Consumer Connected")
        client.subscribe(TOPIC)
        logger.info(f"📡 Subscribed to topic: {TOPIC}")
    else:
        logger.error(f"❌ MQTT Connection Failed (Code: {reason_code})")


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())

        logger.info(f"📩 MQTT Message Received: {payload}")

        # Send message to Celery for asynchronous processing
        save_sensor_data.delay(payload)

    except json.JSONDecodeError:
        logger.error("❌ Invalid JSON received from MQTT broker.")

    except Exception as e:
        logger.exception(f"❌ Error processing MQTT message: {e}")


# -------------------------------------------------
# MQTT Client
# -------------------------------------------------

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message


# -------------------------------------------------
# MQTT Loop
# -------------------------------------------------

def mqtt_loop():
    try:
        client.connect(BROKER, PORT)
        client.loop_forever()

    except Exception as e:
        logger.exception(f"❌ Unable to start MQTT Consumer: {e}")


# -------------------------------------------------
# Start Consumer
# -------------------------------------------------

def start():
    thread = threading.Thread(
        target=mqtt_loop,
        daemon=True,
        name="MQTTConsumerThread",
    )

    thread.start()
