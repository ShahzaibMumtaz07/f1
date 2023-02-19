import csv
import os
from abc import ABC, abstractmethod

from django.conf import settings
from django.core.management.base import BaseCommand

from api.models import *
import unicodedata



class DataLoader(ABC):

    @abstractmethod
    def build(self, row):
        pass

    @abstractmethod
    def save(self, batch):
        pass

    @abstractmethod
    def execute(self):
        pass

class CircuitsLoader(DataLoader):
    def build(self, row):
        row = [x if x != '\\N' else None for x in row]
        id, ref, name, location, country, lat, lng, alt, url  = row
        circuit = Circuits(reference = ref, name = name, location = location, country = country, lat = lat,lng = lng, alt = alt, url = url)
        circuit.id = id
        return circuit
    
    def save(self, batch):
        Circuits.objects.bulk_create(batch)
    
    def execute(self):
        Circuits.objects.all().delete()
        return load_from_csv(os.path.join(settings.BASE_DIR,"media","csv","circuits.csv"),self)

class ConstructorResultsLoader(DataLoader):
    def build(self, row):
        row = [x if x != '\\N' else None for x in row]
        id, race_id, constructor_id, points, status  = row
        constructor_results = ConstructorResults(race_id = race_id, constructor_id = constructor_id, points = points, status = status) 
        constructor_results.id = id
        return constructor_results
    
    def save(self, batch):
        ConstructorResults.objects.bulk_create(batch)
    
    def execute(self):
        ConstructorResults.objects.all().delete()
        return load_from_csv(os.path.join(settings.BASE_DIR,"media","csv","constructor_results.csv"),self)

class ConstructorStandingsLoader(DataLoader):
    def build(self, row):
        row = [x if x != '\\N' else None for x in row]
        id, race_id, constructor_id, points, position, position_text, wins  = row
        constructor_standings = ConstructorStandings(race_id = race_id, constructor_id = constructor_id, points = points,position = position,position_text = position_text, wins = wins) 
        constructor_standings.id = id
        return constructor_standings
    
    def save(self, batch):
        ConstructorStandings.objects.bulk_create(batch)
    
    def execute(self):
        ConstructorStandings.objects.all().delete()
        return load_from_csv(os.path.join(settings.BASE_DIR,"media","csv","constructor_standings.csv"),self)

class ConstructorsLoader(DataLoader):
    def build(self, row):
        row = [x if x != '\\N' else None for x in row]
        id, constructor_ref, name, nationality, url  = row
        constructor = Constructors(constructor_ref = constructor_ref, name = name, nationality = nationality, url=url) 
        constructor.id = id
        return constructor
    
    def save(self, batch):
        Constructors.objects.bulk_create(batch)
    
    def execute(self):
        Constructors.objects.all().delete()
        return load_from_csv(os.path.join(settings.BASE_DIR,"media","csv","constructors.csv"),self)

class DriverStandingsLoader(DataLoader):
    def build(self, row):
        row = [x if x != '\\N' else None for x in row]
        id, race_id,driver_id, points, position, position_text, wins  = row
        driver_standings = DriverStandings(race_id = race_id, driver_id = driver_id, points = points,position = position,position_text = position_text, wins = wins) 
        driver_standings.id = id
        return driver_standings
    
    def save(self, batch):
        DriverStandings.objects.bulk_create(batch)
    
    def execute(self):
        DriverStandings.objects.all().delete()
        return load_from_csv(os.path.join(settings.BASE_DIR,"media","csv","driver_standings.csv"),self)

class DriversLoader(DataLoader):
    def build(self, row):
        row = [x if x != '\\N' else None for x in row]
        
        id, driver_ref, number, code, forename, surname,dob,nationality, url  = row
        forename = strip_accents(forename)
        surname = strip_accents(surname)
        driver = Drivers(driver_ref = driver_ref, number = number, code=code, forename = forename,surname=surname, dob=dob,nationality = nationality, url=url) 
        driver.id = id
        return driver
    
    def save(self, batch):
        Drivers.objects.bulk_create(batch)
    
    def execute(self):
        Drivers.objects.all().delete()
        return load_from_csv(os.path.join(settings.BASE_DIR,"media","csv","drivers.csv"),self)

class LapTimesLoader(DataLoader):
    def build(self, row):
        row = [x if x != '\\N' else None for x in row]
        race_id, driver_id, lap, position, time, milliseconds  = row
        lap_times = LapTimes(race_id = race_id, driver_id = driver_id, lap = lap,position = position, time = time, milliseconds = milliseconds) 
        return lap_times
    
    def save(self, batch):
        LapTimes.objects.bulk_create(batch)
    
    def execute(self):
        LapTimes.objects.all().delete()
        return load_from_csv(os.path.join(settings.BASE_DIR,"media","csv","lap_times.csv"),self)

class PitStopsLoader(DataLoader):
    def build(self, row):
        row = [x if x != '\\N' else None for x in row]
        race_id, driver_id, stop, lap, time, duration,  milliseconds  = row
        pit_stops = PitStops(race_id = race_id, driver_id = driver_id, stop = stop, lap = lap,duration =duration, time = time, milliseconds = milliseconds) 
        return pit_stops
    
    def save(self, batch):
        PitStops.objects.bulk_create(batch)
    
    def execute(self):
        PitStops.objects.all().delete()
        return load_from_csv(os.path.join(settings.BASE_DIR,"media","csv","pit_stops.csv"),self)

class QualifyingLoader(DataLoader):
    def build(self, row):
        row = [x if x != '\\N' else None for x in row]
        id, race_id, driver_id, constructor_id, number, position, q1,q2,q3 = row
        qualifying = Qualifying(race_id = race_id, driver_id = driver_id, constructor_id = constructor_id, number = number, position = position, q1 =q1, q2= q2,q3 = q3) 
        qualifying.id = id
        return qualifying
    
    def save(self, batch):
        Qualifying.objects.bulk_create(batch)
    
    def execute(self):
        Qualifying.objects.all().delete()
        return load_from_csv(os.path.join(settings.BASE_DIR,"media","csv","qualifying.csv"),self)

class RacesLoader(DataLoader):
    def build(self, row):
        row = [x if x != '\\N' else None for x in row]
        id, year,round, circuit_id, name, date, time , url, fp1_date, fp1_time,fp2_date, fp2_time,fp3_date, fp3_time,quali_date, quali_time,sprint_date, sprint_time= row
        race = Races(season = Seasons.objects.get(year = year), round = round, circuit_id= circuit_id, name = name, date=date, time = time, url = url)
        race.id = id
        return race
    
    def save(self, batch):
        Races.objects.bulk_create(batch)
    
    def execute(self):
        Races.objects.all().delete()
        return load_from_csv(os.path.join(settings.BASE_DIR,"media","csv","races.csv"),self)

class ResultsLoader(DataLoader):
    def build(self, row):
        row = [x if x != '\\N' else None for x in row]
        id, race_id, driver_id, constructor_id, number, grid, position, position_text, position_order, points,laps, time, milliseconds, fastest_lap, rank,fastest_lap_time, fastest_lap_speed,status_id = row
        result = Results(race_id = race_id, driver_id = driver_id, constructor_id = constructor_id, number= number, grid = grid, position = position, position_text = position_text, position_order = position_order, points = points, laps = laps, time = time, milliseconds = milliseconds,fastest_lap = fastest_lap,rank = rank, fastest_lap_time = fastest_lap_time,fastest_lap_speed = fastest_lap_speed,status_id =status_id)
        result.id = id
        return result
    
    def save(self, batch):
        Results.objects.bulk_create(batch)
    
    def execute(self):
        Results.objects.all().delete()
        return load_from_csv(os.path.join(settings.BASE_DIR,"media","csv","results.csv"),self)

class SeasonsLoader(DataLoader):
    def build(self, row):
        row = [x if x != '\\N' else None for x in row]
        year, url  = row
        season = Seasons(year = year, url = url)
        return season
    
    def save(self, batch):
        Seasons.objects.bulk_create(batch)
    
    def execute(self):
        Results.objects.all().delete()
        Races.objects.all().delete()
        Seasons.objects.all().delete()
        return load_from_csv(os.path.join(settings.BASE_DIR,"media","csv","seasons.csv"),self)

class StatusLoader(DataLoader):
    def build(self, row):
        row = [x if x != '\\N' else None for x in row]
        id, status  = row
        status_obj = Status(status = status)
        status_obj.id = id
        return status_obj

    def save(self, batch):
        Status.objects.bulk_create(batch)
    
    def execute(self):
        Results.objects.all().delete()
        Races.objects.all().delete()
        Status.objects.all().delete()
        return load_from_csv(os.path.join(settings.BASE_DIR,"media","csv","status.csv"),self)

class SprintResultsLoader(DataLoader):
    def build(self, row):
        row = [x if x != '\\N' else None for x in row]
        id, race_id, driver_id, constructor_id, number, grid, position, position_text, position_order, points,laps, time, milliseconds, fastest_lap, fastest_lap_time,status_id = row
        result = SprintResults(race_id = race_id, driver_id = driver_id, constructor_id = constructor_id, number= number, grid = grid, position = position, position_text = position_text, position_order = position_order, points = points, laps = laps, time = time, milliseconds = milliseconds,fastest_lap = fastest_lap, fastest_lap_time = fastest_lap_time,status_id =status_id)
        result.id = id
        return result
    
    def save(self, batch):
        SprintResults.objects.bulk_create(batch)
    
    def execute(self):
        SprintResults.objects.all().delete()
        return load_from_csv(os.path.join(settings.BASE_DIR,"media","csv","sprint_results.csv"),self)

def load_from_csv(csvpath, loader):
    load_batch = []
    bulk_counter = 0
    MAX_BULK_LOAD = 100
    with open(csvpath, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        row_count = 0
        for row in reader:
            row_count += 1
            if row_count == 1:
                continue  # skip header
            loaded_object = loader.build(row)
            load_batch.append(loaded_object)
            bulk_counter += 1
            if bulk_counter >= MAX_BULK_LOAD:
                loader.save(load_batch)
                load_batch.clear()
                bulk_counter = 0
    if bulk_counter > 0:
        loader.save(load_batch)
    return row_count

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
def clean_existing_objects():
    ConstructorResults.objects.all().delete()
    ConstructorStandings.objects.all().delete()
    DriverStandings.objects.all().delete()
    LapTimes.objects.all().delete()
    PitStops.objects.all().delete()
    Qualifying.objects.all().delete()
    SprintResults.objects.all().delete()
    Results.objects.all().delete()
    Races.objects.all().delete()
    Constructors.objects.all().delete()
    Drivers.objects.all().delete()
    Circuits.objects.all().delete()
    Seasons.objects.all().delete()
    Status.objects.all().delete()

class Command(BaseCommand):

    def handle(self, *args, **options):
        if not Drivers.objects.filter(id = 1).exists():
            clean_existing_objects()
            print("Loading statuses...")
            print(str(StatusLoader().execute()) + " rows loaded")
            print("Loading seasons...")
            print(str(SeasonsLoader().execute()) + " rows loaded")
            print("Loading circuits...")
            print(str(CircuitsLoader().execute()) + " rows loaded")
            print("Loading drivers...")
            print(str(DriversLoader().execute()) + " rows loaded")
            print("Loading contructors units...")
            print(str(ConstructorsLoader().execute()) + " rows loaded")
            print("Loading races...")
            print(str(RacesLoader().execute()) + " rows loaded")
            print("Loading results...")
            print(str(ResultsLoader().execute()) + " rows loaded")
            print("Loading sprint races results...")
            print(str(SprintResultsLoader().execute()) + " rows loaded")
            print("Loading qualifying results...")
            print(str(QualifyingLoader().execute()) + " rows loaded")
            print("Loading pitstops results...")
            print(str(PitStopsLoader().execute()) + " rows loaded")
            print("Loading laptime results...")
            print(str(LapTimesLoader().execute()) + " rows loaded")
            print("Loading driver standings...")
            print(str(DriverStandingsLoader().execute()) + " rows loaded")
            print("Loading constructor standings...")
            print(str(ConstructorStandingsLoader().execute()) + " rows loaded")
            print("Loading constructor results...")
            print(str(ConstructorResultsLoader().execute()) + " rows loaded")
        