from rest_framework import serializers
from .models import Circuits, Drivers, Seasons, Constructors, Status


class CircuitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circuits
        fields = "__all__"


class DriversSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drivers
        fields = "__all__"


class SeasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seasons
        fields = "__all__"


class ConstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constructors
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class AllDriverStandingsSeasonSerializer(serializers.Serializer):
    year = serializers.CharField()
    driver_position = serializers.IntegerField()
    driver_name = serializers.CharField()
    driver_nationality = serializers.CharField()
    constructor_name = serializers.CharField()
    total_points_earned = serializers.FloatField()


class DriverStandingsSeasonSerializer(serializers.Serializer):
    year = serializers.CharField()
    race_name = serializers.CharField()
    race_date = serializers.DateField()
    constructor_name = serializers.CharField()
    race_final_position = serializers.IntegerField()
    race_points_earned = serializers.FloatField()


class AllConstructorSeasonSerializer(serializers.Serializer):
    year = serializers.CharField()
    constructor_position = serializers.IntegerField()
    constructor_name = serializers.CharField()
    total_points_earned = serializers.FloatField()


class ConstructorStandingSeasonSerializer(serializers.Serializer):
    year = serializers.CharField()
    race_name = serializers.CharField()
    race_date = serializers.DateField()
    race_points_earned = serializers.FloatField()

class AllRacesSeasonSerializer(serializers.Serializer):
    race_id = serializers.IntegerField()
    year = serializers.CharField()
    race_name = serializers.CharField()
    race_date = serializers.DateField()
    winner_name = serializers.CharField()
    winner_constructor_name = serializers.CharField()
    winner_race_laps = serializers.IntegerField()
    winner_race_time = serializers.CharField()

class RaceResultSerializer(serializers.Serializer):
    driver_position = serializers.CharField()
    driver_no = serializers.CharField()
    driver_name = serializers.CharField()
    constructor_name = serializers.CharField()
    driver_race_laps = serializers.IntegerField()
    driver_race_time = serializers.CharField()
    driver_race_points = serializers.IntegerField()
    driver_race_status = serializers.CharField()

class RaceFastestLapSerializer(serializers.Serializer):
    driver_position = serializers.CharField()
    driver_no = serializers.CharField()
    driver_name = serializers.CharField()
    constructor_name = serializers.CharField()
    fastest_lap_no = serializers.IntegerField()
    fastest_lap_time = serializers.CharField()
    fastest_lap_avg_speed = serializers.CharField()

class RacePitStopSerialzer(serializers.Serializer):
    stops = serializers.IntegerField()
    driver_no = serializers.CharField()
    driver_name = serializers.CharField()
    constructor_name = serializers.CharField()
    lap_no = serializers.IntegerField()
    pit_stop_time = serializers.CharField()
    pit_stop_duration = serializers.CharField()
    pit_stop_race_duration = serializers.CharField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        duration_ms = int(representation['pit_stop_duration'])
        mm, ss = divmod(duration_ms // 1000, 60)
        ms = duration_ms % 1000
        representation['pit_stop_duration'] = f"{mm:02d}:{ss:02d}:{ms:03d}"
        duration_ms = int(representation['pit_stop_race_duration'])
        mm, ss = divmod(duration_ms // 1000, 60)
        ms = duration_ms % 1000
        representation['pit_stop_race_duration'] = f"{mm:02d}:{ss:02d}:{ms:03d}"
        return representation

class RaceStartGridSerializer(serializers.Serializer):
    driver_position = serializers.CharField()
    driver_no = serializers.CharField()
    driver_name = serializers.CharField()
    constructor_name = serializers.CharField()
    driver_quali_time = serializers.CharField()

class RaceQualifyingSerializer(serializers.Serializer):
    driver_position = serializers.CharField()
    driver_no = serializers.CharField()
    driver_name = serializers.CharField()
    constructor_name = serializers.CharField()
    q1_time = serializers.CharField()
    q2_time = serializers.CharField()
    q3_time = serializers.CharField()