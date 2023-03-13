from django.shortcuts import render


def indexpage(request):
    circuits = Circuits.objects.all().values('lat','lng','name')
    circuits = [dict(item, **{'size':1000 * 4e-4,'color':'white'}) for item in circuits]
    context = {'circuits':circuits}

    return render(request, 'index.html', context)

from rest_framework import generics, filters, views
from django_filters.rest_framework import DjangoFilterBackend
from .models import Circuits, CombinedResults, Constructors, ConstructorStandings, Drivers, Constructors, Results, Seasons, DriverStandings, SprintResults
from .serializers import CircuitsSerializer, DriversSerializer, SeasonsSerializer, ConstructorSerializer, AllDriverStandingsSeasonSerializer, DriverStandingsSeasonSerializer
from django.db.models import Sum, F, Value, Subquery, OuterRef, Max
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber, Concat, Lag
from django.core.cache import cache
from django.conf import settings
from django.utils.functional import cached_property

class CircuitsList(generics.ListAPIView):
    queryset = Circuits.objects.all()
    serializer_class = CircuitsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'country']


class CircuitsDetail(generics.RetrieveAPIView):
    queryset = Circuits.objects.all()
    serializer_class = CircuitsSerializer
    lookup_field = 'id'


class ConstructorsList(generics.ListAPIView):
    queryset = Constructors.objects.all()
    serializer_class = ConstructorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','nationality','country']


class ConstructorsDetail(generics.RetrieveAPIView):
    queryset = Constructors.objects.all()
    serializer_class = ConstructorSerializer
    lookup_field = 'id'

class SeasonsList(generics.ListAPIView):
    queryset = Seasons.objects.all()
    serializer_class = SeasonsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['year']


class SeasonsDetail(generics.RetrieveAPIView):
    queryset = Seasons.objects.all()
    serializer_class = Seasons
    lookup_field = 'id'

class DriversView(generics.ListAPIView):
    serializer_class = DriversSerializer
    queryset = None

    @cached_property
    def cached_queryset(self):
        queryset = Drivers.objects.all()
        driver_id = self.kwargs.get('pk', None)
        year = self.request.query_params.get('year', None)
        cache_key = f"{settings.CACHE_VERSION}_drivers_{driver_id or 'all'}_{year or ''}".rstrip("_")
        if driver_id:
            if year:
                qs_init = CombinedResults.objects.values('race__season').filter(
                    race__season__year = year
                )
                queryset = qs_init.values(
                    'driver'
                ).filter(
                    driver_id = driver_id
                ).annotate(
                    race_name=F('race__name'),
                    race_date=F('race__date'),
                    race_final_position=F('position'),
                    race_points_earned=F('points') if F('points') else F('status__status'),
                    constructor_name=F('constructor__name')
                ).values(
                    'race_name',
                    'race_date',
                    'constructor_name',
                    'race_final_position',
                    'race_points_earned'
                )
                queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)
            else:
                queryset = Drivers.objects.filter(id=driver_id)
                queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)
        else:
            if year:
                qs_init = CombinedResults.objects.values('race__season').filter(
                    race__season__year=year
                )
                queryset = qs_init.annotate(
                    total_points_earned=Sum('points')
                ).annotate(
                    season_position=Window(expression=RowNumber(), order_by=F('total_points_earned').desc())
                ).annotate(
                    driver_position=F('season_position'),
                    driver_name=Concat('driver__forename', Value(' '), 'driver__surname'),
                    driver_nationality=F('driver__country'),
                    constructor_name=F('constructor__name')
                ).values(
                    'driver_position',
                    'driver_name',
                    'driver_nationality',
                    'constructor_name',
                    'total_points_earned'
                ).order_by(
                    '-total_points_earned'
                )
                queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)
            else:
                queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)
        
        return queryset
    
    def get_queryset(self):
        return self.cached_queryset

    def get_serializer_class(self):
        driver_id = self.kwargs.get('pk', None)
        year = self.request.query_params.get('year', None)
        if driver_id:
            if year:
                return DriverStandingsSeasonSerializer
            else:
                return self.serializer_class
        else:
            if year:
                return AllDriverStandingsSeasonSerializer
        return self.serializer_class