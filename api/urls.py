from django.urls import path, re_path
from .views import (
    CircuitsList,
    CircuitsDetail,
    indexpage,
    DriversView,
    ConstructorsView,
    RacesView,
    RacesResultView,
    RaceFastLapView,
    RacePitStopView,
    RaceStartGridView,
    RaceQualifyingView
)

app_name = "api"
urlpatterns = [
    path("world/", indexpage, name="index"),
    path("circuits/", CircuitsList.as_view()),
    path("circuits/<int:id>/", CircuitsDetail.as_view()),
    path("drivers/", DriversView.as_view()),
    path("drivers/<int:pk>/", DriversView.as_view()),
    path("constructors/", ConstructorsView.as_view()),
    path("constructors/<int:pk>/", ConstructorsView.as_view()),
    path("races/", RacesView.as_view()),
    re_path(r'races/(?:(?P<pk>\d+)|(?P<year>\d{4})/(?P<round>\d{1,2}))/race_result/$', RacesResultView.as_view()),
    re_path(r'races/(?:(?P<pk>\d+)|(?P<year>\d{4})/(?P<round>\d{1,2}))/fastest_laps/$', RaceFastLapView.as_view()),
    re_path(r'races/(?:(?P<pk>\d+)|(?P<year>\d{4})/(?P<round>\d{1,2}))/start_grid/$', RaceStartGridView.as_view()),
    re_path(r'races/(?:(?P<pk>\d+)|(?P<year>\d{4})/(?P<round>\d{1,2}))/pit_stops/$', RacePitStopView.as_view()),
    re_path(r'races/(?:(?P<pk>\d+)|(?P<year>\d{4})/(?P<round>\d{1,2}))/qualifying/$', RaceQualifyingView.as_view()),

]
