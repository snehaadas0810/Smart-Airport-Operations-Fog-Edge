class AlertManager:

    def check_alert(self, data):

        alerts = []

        if data.get("passenger_count", 0) > 50:
            alerts.append(
                "High passenger traffic detected."
            )

        data["alerts"] = alerts

        return data