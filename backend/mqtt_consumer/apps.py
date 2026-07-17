from django.apps import AppConfig


class MqttConsumerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mqtt_consumer"

    started = False

    def ready(self):

        if MqttConsumerConfig.started:
            return

        MqttConsumerConfig.started = True

        from . import consumer

        consumer.start()