from .serializers import (
    CircuitsSerializer,
    DriversSerializer,
    ConstructorSerializer,
    AllDriverStandingsSeasonSerializer,
    DriverStandingsSeasonSerializer,
    ConstructorStandingSeasonSerializer,
    AllConstructorSeasonSerializer,
)
from .models import (
    Circuits,
    CombinedResults,
    Constructors,
    Drivers,
    Constructors,
    ConstructorResults,
)
from rest_framework import generics
from .utils import hash_key
from django.utils.functional import cached_property
from django.conf import settings
from django.core.cache import cache
from django.db.models.fields import IntegerField
from django.db.models.functions import RowNumber, Concat
from django.db.models.expressions import Window
from django.db.models import Sum, F, Value, Case, When
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render


def indexpage(request):
    circuits = Circuits.objects.all().values("lat", "lng", "name")
    circuits = [
        dict(item, **{"size": 1000 * 4e-4, "color": "white"}) for item in circuits
    ]
    context = {"circuits": circuits}

    return render(request, "index.html", context)


class CircuitsList(generics.ListAPIView):
    queryset = Circuits.objects.all()
    serializer_class = CircuitsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "country"]


class CircuitsDetail(generics.RetrieveAPIView):
    queryset = Circuits.objects.all()
    serializer_class = CircuitsSerializer
    lookup_field = "id"


class DriversView(generics.ListAPIView):
    serializer_class = DriversSerializer
    queryset = None

    @cached_property
    def cached_queryset(self):
        queryset = Drivers.objects.all()
        driver_id = self.kwargs.get("pk", None)
        year = self.request.query_params.get("year", None)
        if year:
            year = sorted(set([str(x) for x in year.split(",")]))
        cache_key = f"{settings.CACHE_VERSION}_drivers_{driver_id or 'all'}_{year or ''}".rstrip(
            ","
        ).rstrip(
            "_"
        )
        cache_key = hash_key(cache_key)
        if driver_id:
            if year:
                queryset = (
                    CombinedResults.objects.values("race__season")
                    .filter(race__season__year__in=year)
                    .values("driver")
                    .filter(driver_id=driver_id)
                    .annotate(
                        year=F("race__season__year"),
                        race_name=F("race__name"),
                        race_date=F("race__date"),
                        race_final_position=F("position"),
                        race_points_earned=F("points"),
                        constructor_name=F("constructor__name"),
                    )
                    .values(
                        "year",
                        "race_name",
                        "race_date",
                        "constructor_name",
                        "race_final_position",
                        "race_points_earned",
                    )
                    .order_by("year", "race__round")
                )
                queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)
            else:
                queryset = Drivers.objects.filter(id=driver_id)
                queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)
        else:
            if year:
                queryset = (
                    CombinedResults.objects.values("race__season")
                    .filter(race__season__year__in=year)
                    .annotate(total_points_earned=Sum("points"))
                    .annotate(
                        season_position=Window(
                            expression=RowNumber(),
                            order_by=F("total_points_earned").desc(),
                            partition_by=[F("race__season__year")],
                        )
                    )
                    .annotate(
                        year=F("race__season__year"),
                        driver_position=F("season_position"),
                        driver_name=Concat(
                            "driver__forename", Value(" "), "driver__surname"
                        ),
                        driver_nationality=F("driver__country"),
                        constructor_name=F("constructor__name"),
                    )
                    .values(
                        "year",
                        "driver_position",
                        "driver_name",
                        "driver_nationality",
                        "constructor_name",
                        "total_points_earned",
                    )
                    .order_by("year", "-total_points_earned")
                )
                queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)
            else:
                queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)

        return queryset

    def get_queryset(self):
        return self.cached_queryset

    def get_serializer_class(self):
        driver_id = self.kwargs.get("pk", None)
        year = self.request.query_params.get("year", None)
        if driver_id:
            if year:
                return DriverStandingsSeasonSerializer
            else:
                return self.serializer_class
        else:
            if year:
                return AllDriverStandingsSeasonSerializer
        return self.serializer_class


class ConstructorsView(generics.ListAPIView):
    serializer_class = ConstructorSerializer
    queryset = None

    @cached_property
    def cached_queryset(self):
        queryset = Constructors.objects.all()
        constructor_id = self.kwargs.get("pk", None)
        year = self.request.query_params.get("year", None)
        if year:
            year = sorted(set([str(x) for x in year.split(",")]))
        cache_key = f"{settings.CACHE_VERSION}_constructors_{constructor_id or 'all'}_{year or ''}".rstrip(
            ","
        ).rstrip(
            "_"
        )
        cache_key = hash_key(cache_key)
        if constructor_id:
            if year:
                queryset = (
                    ConstructorResults.objects.values("race__season")
                    .filter(
                        race__season__year__in=year,
                    )
                    .values("constructor")
                    .filter(
                        constructor_id=constructor_id,
                    )
                    .annotate(
                        year=F("race__season__year"),
                        race_name=F("race__name"),
                        race_date=F("race__date"),
                        race_points_earned=F("points"),
                    )
                    .values("year", "race_name", "race_date", "race_points_earned")
                    .order_by("year", "race__round")
                )
                queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)
            else:
                queryset = Constructors.objects.filter(id=constructor_id)
                queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)
        else:
            if year:
                queryset = (
                    ConstructorResults.objects.values("race__season")
                    .filter(
                        race__season__year__in=year,
                    )
                    .annotate(
                        total_points_earned=Sum(
                            Case(
                                When(status="D", then=Value(0)),
                                default=F("points"),
                                output_field=IntegerField(),
                            )
                        )
                    )
                    .annotate(
                        season_position=Window(
                            expression=RowNumber(),
                            order_by=F("total_points_earned").desc(),
                            partition_by=[F("race__season__year")],
                        )
                    )
                    .annotate(
                        year=F("race__season__year"),
                        constructor_position=F("season_position"),
                        constructor_name=F("constructor__name"),
                    )
                    .values(
                        "year",
                        "constructor_position",
                        "constructor_name",
                        "total_points_earned",
                    )
                    .order_by("year", "-total_points_earned")
                )
                queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)
            else:
                queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)

        return queryset

    def get_queryset(self):
        return self.cached_queryset

    def get_serializer_class(self):
        constructor_id = self.kwargs.get("pk", None)
        year = self.request.query_params.get("year", None)
        if constructor_id:
            if year:
                return ConstructorStandingSeasonSerializer
            else:
                return self.serializer_class
        else:
            if year:
                return AllConstructorSeasonSerializer
        return self.serializer_class
