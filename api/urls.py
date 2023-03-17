from django.urls import path
from .views import (
    CircuitsList,
    CircuitsDetail,
    indexpage,
    DriversView,
    ConstructorsView,
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
]
