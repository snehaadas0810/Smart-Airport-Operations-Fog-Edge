from rest_framework.decorators import api_view
from rest_framework.response import Response

from airport.models import (
    PassengerData,
    QueueStatus,
    GateStatus,
    TemperatureLog,
    EmergencyAlert,
)


@api_view(["GET"])
def dashboard_data(request):
    try:
        # Latest Records
        passenger = PassengerData.objects.order_by("-received_at").first()
        queue = QueueStatus.objects.order_by("-timestamp").first()
        gate = GateStatus.objects.order_by("-timestamp").first()
        temperature = TemperatureLog.objects.order_by("-timestamp").first()
        alert = EmergencyAlert.objects.order_by("-timestamp").first()

        # Passenger History
        recent_passengers = (
            PassengerData.objects.order_by("-received_at")[:20]
        )

        history = []

        for row in reversed(recent_passengers):
            history.append(
                {
                    "time": row.received_at.strftime("%H:%M:%S")
                    if row.received_at
                    else "--:--:--",
                    "count": row.passenger_count,
                }
            )

        return Response(
            {
                "passengers": (
                    passenger.passenger_count
                    if passenger
                    else 0
                ),

                "flow": (
                    passenger.passenger_flow
                    if passenger
                    else "LOW"
                ),

                "queue": (
                    queue.queue_length
                    if queue
                    else 0
                ),

                "gate": (
                    gate.passengers_waiting
                    if gate
                    else 0
                ),

                "temperature": (
                    round(temperature.temperature, 2)
                    if temperature
                    else 0
                ),

                "alert": (
                    alert.alert_type
                    if alert
                    else "No Alerts"
                ),

                "history": history,
            }
        )

    except Exception as e:
        return Response(
            {
                "error": str(e),
                "passengers": 0,
                "flow": "LOW",
                "queue": 0,
                "gate": 0,
                "temperature": 0,
                "alert": "No Alerts",
                "history": [],
            },
            status=500,
        )
