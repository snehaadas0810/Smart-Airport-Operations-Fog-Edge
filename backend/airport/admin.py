# from django.contrib import admin
# from .models import (
#     Sensor,
#     PassengerData,
#     QueueStatus,
#     GateStatus,
#     TemperatureLog,
#     EmergencyAlert,
# )


# admin.site.register(Sensor)
# admin.site.register(PassengerData)
# admin.site.register(QueueStatus)
# admin.site.register(GateStatus)
# admin.site.register(TemperatureLog)
# admin.site.register(EmergencyAlert)

from django.contrib import admin

from .models import (
    PassengerData,
    QueueStatus,
    GateStatus,
    TemperatureLog,
    EmergencyAlert,
)

admin.site.register(PassengerData)
admin.site.register(QueueStatus)
admin.site.register(GateStatus)
admin.site.register(TemperatureLog)
admin.site.register(EmergencyAlert)