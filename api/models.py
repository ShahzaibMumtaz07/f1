from django.db import models


class Circuits(models.Model):
    reference = models.TextField()
    name = models.TextField()
    location = models.TextField()
    country = models.TextField()
    lat = models.FloatField()
    lng = models.FloatField()
    alt = models.IntegerField(blank=True, null=True)
    url = models.TextField()

    class Meta:
        managed = True
        db_table = 'circuits'


class ConstructorResults(models.Model):
    race = models.ForeignKey('Races',on_delete=models.RESTRICT)
    constructor = models.ForeignKey('Constructors',on_delete=models.RESTRICT)
    points = models.FloatField()
    status = models.TextField(blank=True, null=True) 

    class Meta:
        managed = True
        db_table = 'constructor_results'


class ConstructorStandings(models.Model):
    race = models.ForeignKey('Races',on_delete=models.RESTRICT)
    constructor = models.ForeignKey('Constructors',on_delete=models.RESTRICT)
    points = models.FloatField()
    position = models.IntegerField()
    position_text = models.TextField()
    wins = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'constructor_standings'


class Constructors(models.Model):
    constructor_ref = models.TextField()
    name = models.TextField()
    nationality = models.TextField()
    country = models.TextField(blank=True, null=True)
    url = models.TextField()

    class Meta:
        managed = True
        db_table = 'constructors'


class DriverStandings(models.Model):
    race = models.ForeignKey('Races',on_delete=models.RESTRICT)
    driver = models.ForeignKey('Drivers',on_delete=models.RESTRICT)
    points = models.FloatField()
    position = models.BigIntegerField()
    position_text = models.TextField()
    wins = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'driver_standings'


class Drivers(models.Model):
    driver_ref = models.TextField()
    number = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    forename = models.TextField()
    surname = models.TextField()
    dob = models.DateField()
    nationality = models.TextField()
    country = models.TextField(blank=True, null=True)
    url = models.TextField()

    class Meta:
        managed = True
        db_table = 'drivers'


class LapTimes(models.Model):
    race = models.ForeignKey('Races',on_delete=models.RESTRICT)
    driver = models.ForeignKey('Drivers',on_delete=models.RESTRICT)
    lap = models.IntegerField()
    position = models.IntegerField()
    time = models.TextField()
    milliseconds = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'lap_times'


class PitStops(models.Model):
    race = models.ForeignKey('Races',on_delete=models.RESTRICT)
    driver = models.ForeignKey('Drivers',on_delete=models.RESTRICT)
    stop = models.IntegerField()
    lap = models.IntegerField()
    time = models.TextField()
    duration = models.TextField()
    milliseconds = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'pit_stops'


class Qualifying(models.Model):
    race = models.ForeignKey('Races',on_delete=models.RESTRICT)
    driver = models.ForeignKey('Drivers',on_delete=models.RESTRICT)
    constructor = models.ForeignKey('Constructors',on_delete=models.RESTRICT)
    number = models.IntegerField()
    position = models.IntegerField()
    q1 = models.TextField(blank=True, null=True)
    q2 = models.TextField(blank=True, null=True)
    q3 = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'qualifying'


class Races(models.Model):
    season = models.ForeignKey('Seasons',on_delete=models.RESTRICT)
    round = models.IntegerField()
    circuit = models.ForeignKey('Circuits',on_delete=models.RESTRICT)
    name = models.TextField()
    date = models.DateField()
    time = models.TextField(blank=True, null=True)
    url = models.TextField()

    class Meta:
        managed = True
        db_table = 'races'


class BaseResult(models.Model):

    race = models.ForeignKey('Races', on_delete=models.RESTRICT)
    driver = models.ForeignKey('Drivers', on_delete=models.RESTRICT)
    constructor = models.ForeignKey('Constructors', on_delete=models.RESTRICT)
    number = models.TextField(blank=True, null=True)
    grid = models.IntegerField()
    position = models.TextField(blank=True, null=True)
    position_text = models.TextField(blank=True, null=True)
    position_order = models.IntegerField()
    points = models.FloatField()
    laps = models.IntegerField()
    time = models.TextField(blank=True, null=True)
    milliseconds = models.TextField(blank=True, null=True)
    fastest_lap = models.IntegerField(blank=True, null=True)
    fastest_lap_time = models.TextField(blank=True, null=True)
    status = models.ForeignKey('Status', on_delete=models.RESTRICT)

    class Meta:
        abstract = True


class Results(BaseResult):

    rank = models.IntegerField(blank=True, null=True)
    fastest_lap_speed = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'results'


class SprintResults(BaseResult):

    class Meta:
        managed = True
        db_table = 'sprint_results'


class CombinedResults(BaseResult):

    rank = models.IntegerField(blank=True, null=True)
    fastest_lap_speed = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'combined_results'


class Seasons(models.Model):
    year = models.TextField()
    url = models.TextField()

    class Meta:
        managed = True
        db_table = 'seasons'


class Status(models.Model):
    status = models.TextField()
    class Meta:
        managed = True
        db_table = 'status'