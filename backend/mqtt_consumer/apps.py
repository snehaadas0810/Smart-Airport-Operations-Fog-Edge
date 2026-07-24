import sys

from django.apps import AppConfig


class MqttConsumerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mqtt_consumer"

    started = False

    def ready(self):
        # Start the MQTT consumer only when running the Django development server
        if "runserver" not in sys.argv:
            return

        # Prevent multiple starts in the same process
        if MqttConsumerConfig.started:
            return

        MqttConsumerConfig.started = True

        from . import consumer

        consumer.start()
