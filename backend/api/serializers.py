from rest_framework import serializers
from airport.models import PassengerData


class PassengerSerializer(serializers.ModelSerializer):

    class Meta:
        model = PassengerData
        fields = "__all__"  