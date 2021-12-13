# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Circuits(models.Model):
    circuitid = models.BigIntegerField(db_column='circuitId', blank=True, null=True)  # Field name made lowercase.
    circuitref = models.TextField(db_column='circuitRef', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    alt = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'circuits'


class ConstructorResults(models.Model):
    constructorresultsid = models.BigIntegerField(db_column='constructorResultsId', blank=True, null=True)  # Field name made lowercase.
    raceid = models.BigIntegerField(db_column='raceId', blank=True, null=True)  # Field name made lowercase.
    constructorid = models.BigIntegerField(db_column='constructorId', blank=True, null=True)  # Field name made lowercase.
    points = models.FloatField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'constructor_results'


class ConstructorStandings(models.Model):
    constructorstandingsid = models.BigIntegerField(db_column='constructorStandingsId', blank=True, null=True)  # Field name made lowercase.
    raceid = models.BigIntegerField(db_column='raceId', blank=True, null=True)  # Field name made lowercase.
    constructorid = models.BigIntegerField(db_column='constructorId', blank=True, null=True)  # Field name made lowercase.
    points = models.FloatField(blank=True, null=True)
    position = models.BigIntegerField(blank=True, null=True)
    positiontext = models.TextField(db_column='positionText', blank=True, null=True)  # Field name made lowercase.
    wins = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'constructor_standings'


class Constructors(models.Model):
    constructorid = models.BigIntegerField(db_column='constructorId', blank=True, null=True)  # Field name made lowercase.
    constructorref = models.TextField(db_column='constructorRef', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(blank=True, null=True)
    nationality = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'constructors'


class DriverStandings(models.Model):
    driverstandingsid = models.BigIntegerField(db_column='driverStandingsId', blank=True, null=True)  # Field name made lowercase.
    raceid = models.BigIntegerField(db_column='raceId', blank=True, null=True)  # Field name made lowercase.
    driverid = models.BigIntegerField(db_column='driverId', blank=True, null=True)  # Field name made lowercase.
    points = models.FloatField(blank=True, null=True)
    position = models.BigIntegerField(blank=True, null=True)
    positiontext = models.TextField(db_column='positionText', blank=True, null=True)  # Field name made lowercase.
    wins = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'driver_standings'


class Drivers(models.Model):
    driverid = models.BigIntegerField(db_column='driverId', blank=True, null=True)  # Field name made lowercase.
    driverref = models.TextField(db_column='driverRef', blank=True, null=True)  # Field name made lowercase.
    number = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    forename = models.TextField(blank=True, null=True)
    surname = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    nationality = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drivers'


class LapTimes(models.Model):
    raceid = models.BigIntegerField(db_column='raceId', blank=True, null=True)  # Field name made lowercase.
    driverid = models.BigIntegerField(db_column='driverId', blank=True, null=True)  # Field name made lowercase.
    lap = models.BigIntegerField(blank=True, null=True)
    position = models.BigIntegerField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    milliseconds = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lap_times'


class PitStops(models.Model):
    raceid = models.BigIntegerField(db_column='raceId', blank=True, null=True)  # Field name made lowercase.
    driverid = models.BigIntegerField(db_column='driverId', blank=True, null=True)  # Field name made lowercase.
    stop = models.BigIntegerField(blank=True, null=True)
    lap = models.BigIntegerField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    duration = models.TextField(blank=True, null=True)
    milliseconds = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pit_stops'


class Qualifying(models.Model):
    qualifyid = models.BigIntegerField(db_column='qualifyId', blank=True, null=True)  # Field name made lowercase.
    raceid = models.BigIntegerField(db_column='raceId', blank=True, null=True)  # Field name made lowercase.
    driverid = models.BigIntegerField(db_column='driverId', blank=True, null=True)  # Field name made lowercase.
    constructorid = models.BigIntegerField(db_column='constructorId', blank=True, null=True)  # Field name made lowercase.
    number = models.BigIntegerField(blank=True, null=True)
    position = models.BigIntegerField(blank=True, null=True)
    q1 = models.TextField(blank=True, null=True)
    q2 = models.TextField(blank=True, null=True)
    q3 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qualifying'


class Races(models.Model):
    raceid = models.BigIntegerField(db_column='raceId', blank=True, null=True)  # Field name made lowercase.
    year = models.BigIntegerField(blank=True, null=True)
    round = models.BigIntegerField(blank=True, null=True)
    circuitid = models.BigIntegerField(db_column='circuitId', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'races'


class Results(models.Model):
    resultid = models.BigIntegerField(db_column='resultId', blank=True, null=True)  # Field name made lowercase.
    raceid = models.BigIntegerField(db_column='raceId', blank=True, null=True)  # Field name made lowercase.
    driverid = models.BigIntegerField(db_column='driverId', blank=True, null=True)  # Field name made lowercase.
    constructorid = models.BigIntegerField(db_column='constructorId', blank=True, null=True)  # Field name made lowercase.
    number = models.TextField(blank=True, null=True)
    grid = models.BigIntegerField(blank=True, null=True)
    position = models.TextField(blank=True, null=True)
    positiontext = models.TextField(db_column='positionText', blank=True, null=True)  # Field name made lowercase.
    positionorder = models.BigIntegerField(db_column='positionOrder', blank=True, null=True)  # Field name made lowercase.
    points = models.FloatField(blank=True, null=True)
    laps = models.BigIntegerField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    milliseconds = models.TextField(blank=True, null=True)
    fastestlap = models.TextField(db_column='fastestLap', blank=True, null=True)  # Field name made lowercase.
    rank = models.TextField(blank=True, null=True)
    fastestlaptime = models.TextField(db_column='fastestLapTime', blank=True, null=True)  # Field name made lowercase.
    fastestlapspeed = models.TextField(db_column='fastestLapSpeed', blank=True, null=True)  # Field name made lowercase.
    statusid = models.BigIntegerField(db_column='statusId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'results'


class Seasons(models.Model):
    year = models.BigIntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seasons'


class Status(models.Model):
    statusid = models.BigIntegerField(db_column='statusId', blank=True, null=True)  # Field name made lowercase.
    status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status'
