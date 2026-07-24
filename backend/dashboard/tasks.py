import logging

from celery import shared_task
from django.utils.dateparse import parse_datetime

from airport.models import (
    PassengerData,
    QueueStatus,
    GateStatus,
    TemperatureLog,
    EmergencyAlert,
)


logger = logging.getLogger(__name__)


@shared_task(ignore_result=True)
def save_sensor_data(payload):
    try:
        sensor_type = payload.get("sensor_type")

        # -------------------------------------------------
        # Passenger Counter
        # -------------------------------------------------
        if sensor_type == "Passenger Counter":

            PassengerData.objects.create(
                sensor_id=payload["sensor_id"],
                location=payload["location"],
                passenger_count=payload["passenger_count"],
                passenger_flow=payload["passenger_flow"],
                edge_timestamp=parse_datetime(payload["edge_timestamp"]),
            )

            logger.info("✅ Passenger data saved.")

        # -------------------------------------------------
        # Queue Sensor
        # -------------------------------------------------
        elif sensor_type == "Queue Sensor":

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

            logger.info("✅ Queue data saved.")

        # -------------------------------------------------
        # Gate Sensor
        # -------------------------------------------------
        elif sensor_type == "Gate Sensor":

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

            logger.info("✅ Gate data saved.")

        # -------------------------------------------------
        # Temperature Sensor
        # -------------------------------------------------
        elif sensor_type == "Temperature":

            TemperatureLog.objects.create(
                sensor_id=payload["sensor_id"],
                location=payload["location"],
                temperature=payload["temperature"],
            )

            logger.info("✅ Temperature data saved.")

        # -------------------------------------------------
        # Emergency Alert
        # -------------------------------------------------
        elif sensor_type == "Emergency":

            EmergencyAlert.objects.create(
                alert_type=payload["alert_type"],
                location=payload["location"],
                description=payload["description"],
                resolved=False,
            )

            logger.info("✅ Emergency alert saved.")

        else:
            logger.warning(f"⚠ Unknown sensor type received: {sensor_type}")

    except KeyError as e:
        logger.error(f"❌ Missing required field: {e}")

    except Exception as e:
        logger.exception(f"❌ Error saving sensor data: {e}")
