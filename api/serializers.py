from rest_framework import serializers
from .models import Circuits, Drivers


class CircuitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circuits
        fields = '__all__'

class DriversSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drivers
        fields = '__all__'
