from rest_framework import serializers
from .models import Circuits, Drivers, Results,Seasons, Constructors, Status, DriverStandings


class CircuitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circuits
        fields = '__all__'

class DriversSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drivers
        fields = '__all__'

class SeasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seasons
        fields = '__all__'

class ConstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constructors
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class AllDriverStandingsSeasonSerializer(serializers.Serializer):
    driver_position = serializers.IntegerField()
    driver_name = serializers.CharField()
    driver_nationality = serializers.CharField()
    constructor_name = serializers.CharField()
    total_points_earned = serializers.FloatField()


class DriverStandingsSeasonSerializer(serializers.Serializer):
    race_name = serializers.CharField()
    race_date = serializers.DateField()
    constructor_name = serializers.CharField()
    race_final_position = serializers.IntegerField()
    race_points_earned = serializers.FloatField()

