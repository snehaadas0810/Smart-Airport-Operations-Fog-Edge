class PassengerAnalytics:

    def analyze(self, data):

        passengers = data.get("passenger_count", 0)

        if passengers < 20:
            level = "LOW"

        elif passengers < 40:
            level = "MEDIUM"

        else:
            level = "HIGH"

        data["passenger_flow"] = level

        return data