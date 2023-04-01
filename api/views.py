from .serializers import (
    CircuitsSerializer,
    DriversSerializer,
    ConstructorSerializer,
    AllDriverStandingsSeasonSerializer,
    DriverStandingsSeasonSerializer,
    ConstructorStandingSeasonSerializer,
    AllConstructorSeasonSerializer,
    AllRacesSeasonSerializer,
    RacePitStopSerialzer,
    RaceResultSerializer,
    RaceFastestLapSerializer,
    RaceStartGridSerializer,
    RaceQualifyingSerializer,
)
from .models import (
    Circuits,
    CombinedResults,
    Constructors,
    Drivers,
    Constructors,
    ConstructorResults,
    PitStops,
    Qualifying,
    Races,
    Results,
)
from rest_framework import generics
from .utils import hash_key
from django.utils.functional import cached_property
from django.conf import settings
from django.core.cache import cache
from django.db.models.fields import IntegerField, CharField
from django.db.models.functions import RowNumber, Concat, Cast, Coalesce
from django.db.models.expressions import Window
from django.db.models import Sum, F, Value, Case, When, Q
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.db.models import Subquery, OuterRef


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


class RacesView(generics.ListAPIView):
    serializer_class = AllRacesSeasonSerializer
    queryset = None

    @cached_property
    def cached_queryset(self):
        queryset = Results.objects.none()
        year = self.request.query_params.get("year", None)
        if year:
            year = sorted(set([str(x) for x in year.split(",")]))
        else:
            return queryset
        cache_key = f"{settings.CACHE_VERSION}_races_all_{year}"
        cache_key = hash_key(cache_key)
        queryset = (
            Results.objects.filter(race__season__year__in=year, position=1)
            .select_related("race__season", "race__circuit", "driver", "constructor")
            .annotate(
                year=F("race__season__year"),
                race_name=F("race__name"),
                race_date=F("race__date"),
                winner_name=Concat("driver__forename", Value(" "), "driver__surname"),
                winner_constructor_name=F("constructor__name"),
                winner_race_laps=F("laps"),
                winner_race_time=F("time"),
            )
            .order_by("race__date")
            .values(
                "race_id",
                "year",
                "race_name",
                "race_date",
                "winner_name",
                "winner_constructor_name",
                "winner_race_laps",
                "winner_race_time",
            )
        )
        queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)
        return queryset

    def get_queryset(self):
        return self.cached_queryset


class RacesResultView(generics.ListAPIView):
    serializer_class = RaceResultSerializer
    queryset = None

    @cached_property
    def cached_queryset(self):
        queryset = Results.objects.none()
        race_id = self.kwargs.get("pk", None)
        year = self.kwargs.get("year", None)
        round = self.kwargs.get("round", None)
        if race_id:
            queryset = Results.objects.filter(race_id=race_id)
            cache_key = f"{settings.CACHE_VERSION}_race_results_{race_id}"
        elif year and round:
            queryset = Results.objects.filter(
                race__season__year=year, race__round=round
            )
            cache_key = f"{settings.CACHE_VERSION}_race_results_{year}_{round}"
        else:
            return queryset

        cache_key = hash_key(cache_key)
        queryset = (
            queryset.select_related("driver", "constructor")
            .annotate(
                driver_position=Case(
                    When(position=None, then=Value("Not Completed")),
                    default=Cast(F("position"), CharField()),
                    output_field=CharField(),
                ),
                driver_no=F("number"),
                driver_name=Concat("driver__forename", Value(" "), "driver__surname"),
                constructor_name=F("constructor__name"),
                driver_race_laps=F("laps"),
                driver_race_time=F("time"),
                driver_race_points=F("points"),
                driver_race_status=F("status__status"),
            )
            .order_by("position")
            .values(
                "driver_position",
                "driver_no",
                "driver_name",
                "constructor_name",
                "driver_race_laps",
                "driver_race_time",
                "driver_race_points",
                "driver_race_status",
            )
        )
        queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)
        return queryset

    def get_queryset(self):
        return self.cached_queryset


class RaceFastLapView(generics.ListAPIView):
    serializer_class = RaceFastestLapSerializer
    queryset = None

    @cached_property
    def cached_queryset(self):
        queryset = Results.objects.none()
        race_id = self.kwargs.get("pk", None)
        year = self.kwargs.get("year", None)
        round = self.kwargs.get("round", None)
        if race_id:
            queryset = Results.objects.filter(race_id=race_id)
            cache_key = f"{settings.CACHE_VERSION}_race_fastest_laps_{race_id}"
        elif year and round:
            queryset = Results.objects.filter(
                race__season__year=year, race__round=round
            )
            cache_key = f"{settings.CACHE_VERSION}_race_fastest_laps_{year}_{round}"
        else:
            return queryset

        cache_key = hash_key(cache_key)
        queryset = (
            queryset.filter(fastest_lap_time__isnull=False)
            .select_related("driver", "constructor")
            .annotate(
                driver_position=Window(
                    expression=RowNumber(),
                    order_by=F("fastest_lap_time").asc(),
                ),
                driver_no=F("number"),
                driver_name=Concat("driver__forename", Value(" "), "driver__surname"),
                constructor_name=F("constructor__name"),
                fastest_lap_no=F("fastest_lap"),
                fastest_lap_avg_speed=F("fastest_lap_speed"),
            )
            .values(
                "driver_position",
                "driver_no",
                "driver_name",
                "constructor_name",
                "fastest_lap_no",
                "fastest_lap_time",
                "fastest_lap_avg_speed",
            )
        )
        queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)
        return queryset

    def get_queryset(self):
        return self.cached_queryset


class RacePitStopView(generics.ListAPIView):
    serializer_class = RacePitStopSerialzer
    queryset = None

    @cached_property
    def cached_queryset(self):
        queryset = PitStops.objects.none()
        race_id = self.kwargs.get("pk", None)
        year = self.kwargs.get("year", None)
        round = self.kwargs.get("round", None)
        if race_id:
            results = Results.objects.filter(race_id=race_id)
            queryset = (
                PitStops.objects.filter(race_id=race_id)
                .annotate(
                    stops=F("stop"),
                    driver_no=Subquery(
                        results.filter(driver_id=OuterRef("driver_id")).values(
                            "number"
                        )[:1]
                    ),
                    driver_name=Concat(
                        "driver__forename", Value(" "), "driver__surname"
                    ),
                    constructor_name=Subquery(
                        results.filter(driver_id=OuterRef("driver_id")).values(
                            "constructor__name"
                        )[:1]
                    ),
                    lap_no=F("lap"),
                    pit_stop_time=F("time"),
                    pit_stop_duration=F("milliseconds"),
                    pit_stop_race_duration=Window(
                        expression=Sum("milliseconds"),
                        partition_by=F("driver_id"),
                        order_by=F("stop").asc(),
                    ),
                )
                .order_by("time")
                .values(
                    "stops",
                    "driver_no",
                    "driver_name",
                    "constructor_name",
                    "lap_no",
                    "pit_stop_time",
                    "pit_stop_duration",
                    "pit_stop_race_duration",
                )
            )
            cache_key = f"{settings.CACHE_VERSION}_race_pit_stops_{race_id}"
        elif year and round:
            results = Results.objects.filter(race__season__year=year, race__round=round)
            queryset = (
                PitStops.objects.filter(race__season__year=year, race__round=round)
                .annotate(
                    stops=F("stop"),
                    driver_no=Subquery(
                        results.filter(driver_id=OuterRef("driver_id")).values(
                            "number"
                        )[:1]
                    ),
                    driver_name=Concat(
                        "driver__forename", Value(" "), "driver__surname"
                    ),
                    constructor_name=Subquery(
                        results.filter(driver_id=OuterRef("driver_id")).values(
                            "constructor__name"
                        )[:1]
                    ),
                    lap_no=F("lap"),
                    pit_stop_time=F("time"),
                    pit_stop_duration=F("milliseconds"),
                    pit_stop_race_duration=Window(
                        expression=Sum("milliseconds"),
                        partition_by=F("driver_id"),
                        order_by=F("stop").asc(),
                    ),
                )
                .order_by("time")
                .values(
                    "stops",
                    "driver_no",
                    "driver_name",
                    "constructor_name",
                    "lap_no",
                    "pit_stop_time",
                    "pit_stop_duration",
                    "pit_stop_race_duration",
                )
            )
            cache_key = f"{settings.CACHE_VERSION}_race_pit_stops_{year}_{round}"
        else:
            return queryset

        cache_key = hash_key(cache_key)
        queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)
        return queryset

    def get_queryset(self):
        return self.cached_queryset


class RaceStartGridView(generics.ListAPIView):
    serializer_class = RaceStartGridSerializer
    queryset = None

    @cached_property
    def cached_queryset(self):
        queryset = Results.objects.none()
        race_id = self.kwargs.get("pk", None)
        year = self.kwargs.get("year", None)
        round = self.kwargs.get("round", None)

        if race_id:
            subquery = (
                Qualifying.objects.filter(
                    Q(driver_id=OuterRef("driver_id"), race_id=race_id),
                    Q(q3__isnull=False) | Q(q2__isnull=False) | Q(q1__isnull=False),
                )
                .order_by("-q3", "-q2", "-q1")
                .values("q3", "q2", "q1")[:1]
                .annotate(
                    driver_quali_time=Coalesce(
                        "q3",
                        "q2",
                        "q1",
                        output_field=CharField(),
                    )
                )
            )

            results = (
                Results.objects.filter(race_id=race_id)
                .select_related("driver", "constructor")
                .annotate(
                    driver_no=F("number"),
                    driver_name=Concat(
                        "driver__forename", Value(" "), "driver__surname"
                    ),
                    constructor_name=F("constructor__name"),
                    driver_quali_time=Subquery(subquery.values("driver_quali_time")),
                    grid_order=Case(
                        When(grid=0, then=Value(2147483647)),
                        default=F("grid"),
                        output_field=IntegerField(),
                    ),
                )
                .order_by("grid_order")
            )
            cache_key = f"{settings.CACHE_VERSION}_race_start_grid_{race_id}"
        elif year and round:
            subquery = (
                Qualifying.objects.filter(
                    Q(
                        driver_id=OuterRef("driver_id"),
                        race__season__year=year,
                        race__round=round,
                    ),
                    Q(q3__isnull=False) | Q(q2__isnull=False) | Q(q1__isnull=False),
                )
                .order_by("-q3", "-q2", "-q1")
                .values("q3", "q2", "q1")[:1]
                .annotate(
                    driver_quali_time=Coalesce(
                        "q3",
                        "q2",
                        "q1",
                        output_field=CharField(),
                    )
                )
            )

            results = (
                Results.objects.filter(race__season__year=year, race__round=round)
                .select_related("driver", "constructor")
                .annotate(
                    driver_no=F("number"),
                    driver_name=Concat(
                        "driver__forename", Value(" "), "driver__surname"
                    ),
                    constructor_name=F("constructor__name"),
                    driver_quali_time=Subquery(subquery.values("driver_quali_time")),
                    grid_order=Case(
                        When(grid=0, then=Value(2147483647)),
                        default=F("grid"),
                        output_field=IntegerField(),
                    ),
                )
                .order_by("grid_order")
            )
            cache_key = f"{settings.CACHE_VERSION}_start_grid_{year}_{round}"
        else:
            return queryset

        cache_key = hash_key(cache_key)

        queryset = results.annotate(
            driver_position=Window(
                expression=RowNumber(), order_by=F("grid_order").asc()
            ),
        ).values(
            "driver_position",
            "driver_no",
            "driver_name",
            "constructor_name",
            "driver_quali_time",
        )
        queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)
        return queryset

    def get_queryset(self):
        return self.cached_queryset


class RaceQualifyingView(generics.ListAPIView):
    serializer_class = RaceQualifyingSerializer
    queryset = None

    @cached_property
    def cached_queryset(self):
        queryset = Qualifying.objects.none()
        race_id = self.kwargs.get("pk", None)
        year = self.kwargs.get("year", None)
        round = self.kwargs.get("round", None)

        if race_id:
            queryset = Qualifying.objects.filter(race_id=race_id)
            cache_key = f"{settings.CACHE_VERSION}_race_qualifying_{race_id}"
        elif year and round:
            queryset = Qualifying.objects.filter(
                race__season__year=year, race__round=round
            )
            cache_key = f"{settings.CACHE_VERSION}_race_qualifying_{year}_{round}"
        else:
            return queryset

        cache_key = hash_key(cache_key)

        queryset = (
            queryset.annotate(
                driver_position=F("position"),
                driver_no=F("number"),
                driver_name=Concat("driver__forename", Value(" "), "driver__surname"),
                constructor_name=F("constructor__name"),
                q1_time=F("q1"),
                q2_time=F("q2"),
                q3_time=F("q3"),
            )
            .values(
                "driver_position",
                "driver_no",
                "driver_name",
                "constructor_name",
                "q1_time",
                "q2_time",
                "q3_time",
            )
            .order_by("driver_position")
        )
        queryset = cache.get_or_set(cache_key, queryset, settings.CACHE_TIMEOUT)
        return queryset

    def get_queryset(self):
        return self.cached_queryset
