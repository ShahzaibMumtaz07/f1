from django.urls import include, path
from rest_framework import routers
from .views import CircuitsList, CircuitsDetail, DriversList, DriversDetail, indexpage

app_name = "api"
urlpatterns = [
    path('world/', indexpage, name = 'index'),
    path(r'circuits/', CircuitsList.as_view()),
    path(r'circuits/<int:pk>', CircuitsDetail.as_view()),
    path(r'drivers/', DriversList.as_view()),
    path(r'drivers/<int:pk>', DriversDetail.as_view()),
]
