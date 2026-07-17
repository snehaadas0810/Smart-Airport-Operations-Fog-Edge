# # from rest_framework.response import Response
# # from rest_framework.decorators import api_view

# # from airport.models import PassengerData
# # from .serializers import PassengerSerializer


# # @api_view(['GET'])
# # def passenger_list(request):

# #     passengers = PassengerData.objects.all().order_by("-received_at")

# #     serializer = PassengerSerializer(passengers, many=True)

# #     return Response(serializer.data)


# # @api_view(['GET'])
# # def latest_passenger(request):

# #     passenger = PassengerData.objects.last()

# #     serializer = PassengerSerializer(passenger)

# #     return Response(serializer.data)

# ###########new.........new /////////////////////////////////////////

# # from rest_framework.decorators import api_view
# # from rest_framework.response import Response

# # from airport.models import PassengerData


# # @api_view(['GET'])
# # def dashboard_data(request):

# #     latest = PassengerData.objects.order_by('-received_at').first()

# #     if latest:

# #         data = {
# #             "passenger_count": latest.passenger_count,
# #             "passenger_flow": latest.passenger_flow,
# #             "location": latest.location,
# #             "timestamp": latest.received_at,
# #         }

# #     else:

# #         data = {
# #             "passenger_count": 0,
# #             "passenger_flow": "LOW",
# #             "location": "N/A",
# #             "timestamp": None,
# #         }

# #     return Response(data)

# ###########################new.....new/////////////////////////////


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from airport.models import PassengerData

# from airport.models import (
#     PassengerData,
#     QueueStatus,
#     GateStatus,
#     TemperatureLog,
#     EmergencyAlert
# )


# @api_view(["GET"])
# # def dashboard_data(request):

# #     passenger = PassengerData.objects.order_by("-received_at").first()
# #     queue = QueueStatus.objects.order_by("-timestamp").first()
# #     gate = GateStatus.objects.order_by("-timestamp").first()
# #     temp = TemperatureLog.objects.order_by("-timestamp").first()
# #     alert = EmergencyAlert.objects.order_by("-timestamp").first()

# #     return Response({

# #         "passengers":
# #             passenger.passenger_count if passenger else 0,

# #         "passenger_flow":
# #             passenger.passenger_flow if passenger else "LOW",

# #         "queue_length":
# #             queue.queue_length if queue else 0,

# #         "gate_waiting":
# #             gate.passengers_waiting if gate else 0,

# #         "temperature":
# #             temp.temperature if temp else 0,

# #         "alert":
# #             alert.alert_type if alert else "No Alerts"

# #     })

# def dashboard_data(request):

#     latest = PassengerData.objects.order_by("-received_at").first()

#     recent = PassengerData.objects.order_by("-received_at")[:20]

#     history = []

#     for row in reversed(recent):

#         history.append({
#             "time": row.received_at.strftime("%H:%M:%S"),
#             "count": row.passenger_count
#         })

#     if latest:

#         return Response({

#             "passengers": latest.passenger_count,

#             "flow": latest.passenger_flow,

#             "location": latest.location,

#             "history": history

#         })

#     return Response({

#         "passengers": 0,

#         "flow": "LOW",

#         "location": "N/A",

#         "history": []

#     })

###########################new.....new/////////////////////////////

from rest_framework.decorators import api_view
from rest_framework.response import Response

from airport.models import (
    PassengerData,
    QueueStatus,
    GateStatus,
    TemperatureLog,
    EmergencyAlert
)


@api_view(["GET"])
def dashboard_data(request):

    passenger = PassengerData.objects.order_by("-received_at").first()
    queue = QueueStatus.objects.order_by("-timestamp").first()
    gate = GateStatus.objects.order_by("-timestamp").first()
    temp = TemperatureLog.objects.order_by("-timestamp").first()
    alert = EmergencyAlert.objects.order_by("-timestamp").first()

    recent = PassengerData.objects.order_by("-received_at")[:20]

    history = []

    for row in reversed(recent):
        history.append({
            "time": row.received_at.strftime("%H:%M:%S"),
            "count": row.passenger_count
        })

    return Response({

        "passengers":
            passenger.passenger_count if passenger else 0,

        "flow":
            passenger.passenger_flow if passenger else "LOW",

        "queue":
            queue.queue_length if queue else 0,

        "gate":
            gate.passengers_waiting if gate else 0,

        "temperature":
            temp.temperature if temp else 0,

        "alert":
            alert.alert_type if alert else "No Alerts",

        "history":
            history

    })