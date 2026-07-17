from django.db import models


class Sensor(models.Model):

    SENSOR_TYPES = [
        ('PASSENGER', 'Passenger Counter'),
        ('QUEUE', 'Queue Sensor'),
        ('GATE', 'Gate Occupancy'),
        ('TEMP', 'Temperature'),
        ('EMERGENCY', 'Emergency'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    sensor_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor_id} - {self.name}"
    
class PassengerData(models.Model):

    sensor_id = models.CharField(max_length=20)

    location = models.CharField(max_length=100)

    passenger_count = models.IntegerField()

    passenger_flow = models.CharField(max_length=20)

    edge_timestamp = models.DateTimeField()

    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor_id} - {self.passenger_count}"

    # sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)

    # passenger_count = models.IntegerField()

    # timestamp = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.sensor.name} - {self.passenger_count}"
    
class QueueStatus(models.Model):

    area = models.CharField(max_length=100)

    queue_length = models.IntegerField()

    waiting_time = models.FloatField()

    congestion_level = models.CharField(max_length=20)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.area
    
class GateStatus(models.Model):

    gate_name = models.CharField(max_length=20)

    passengers_waiting = models.IntegerField()

    status = models.CharField(max_length=20)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.gate_name
    
class TemperatureLog(models.Model):

    sensor_id = models.CharField(max_length=20)

    location = models.CharField(max_length=100)

    temperature = models.FloatField()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor_id} - {self.temperature}°C"
    
class EmergencyAlert(models.Model):

    ALERT_TYPES = [
        ('FIRE', 'Fire'),
        ('SMOKE', 'Smoke'),
        ('MEDICAL', 'Medical'),
        ('SECURITY', 'Security'),
    ]

    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)

    location = models.CharField(max_length=100)

    description = models.TextField()

    resolved = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.alert_type