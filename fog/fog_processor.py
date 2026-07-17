from analytics import PassengerAnalytics
from alert_manager import AlertManager
from publisher import FogPublisher


class FogProcessor:

    def __init__(self):

        self.analytics = PassengerAnalytics()

        self.alerts = AlertManager()

        self.publisher = FogPublisher()

    def process(self, data):

        sensor = data.get("sensor_type")

        if sensor == "Passenger Counter":

            data = self.analytics.analyze(data)

        data = self.alerts.check_alert(data)

        print("\nFOG PROCESSING")
        print(data)

        self.publisher.publish(data)
