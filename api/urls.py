from django.urls import include, path
from rest_framework import routers
from .views import CircuitsList \
                    , CircuitsDetail \
                    , indexpage \
                    , ConstructorsDetail \
                    , ConstructorsList \
                    , SeasonsList \
                    , SeasonsDetail \
                    , DriversView

app_name = "api"
urlpatterns = [
    path('world/', indexpage, name = 'index'),
    path(r'circuits/', CircuitsList.as_view()),
    path(r'circuits/<int:id>/', CircuitsDetail.as_view()),
    path(r'drivers/', DriversView.as_view()),
    path(r'drivers/<int:pk>/', DriversView.as_view()),
    path(r'constructors/', ConstructorsList.as_view()),
    path(r'constructors/<int:id>/', ConstructorsDetail.as_view()),
    path(r'seasons/', SeasonsList.as_view()),
    path(r'seasons/<int:id>/', SeasonsDetail.as_view()),
]
