from django.shortcuts import render

def indexpage(request):
    circuits = Circuits.objects.all().values('lat','lng','name')
    circuits = [dict(item, **{'size':1000 * 4e-4,'color':'white'}) for item in circuits]
    context = {'circuits':circuits}

    return render(request, 'index.html', context)

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Circuits, Drivers, Constructors, Seasons
from .serializers import CircuitsSerializer, DriversSerializer


class CircuitsList(generics.ListAPIView):
    queryset = Circuits.objects.all()
    serializer_class = CircuitsSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name', 'country']
    # search_fields = ['name', 'country']
    # ordering_fields = ['id', 'name', 'country']


class CircuitsDetail(generics.RetrieveAPIView):
    queryset = Circuits.objects.all()
    serializer_class = CircuitsSerializer
    lookup_field = 'id'


class DriversList(generics.ListAPIView):
    queryset = Drivers.objects.all()
    serializer_class = DriversSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'forename', 'surname', 'dob', 'nationality']
    # search_fields = ['forename', 'surname', 'nationality']
    # ordering_fields = ['id', 'name', 'country']


class DriversDetail(generics.RetrieveAPIView):
    queryset = Drivers.objects.all()
    serializer_class = DriversSerializer
    lookup_field = 'id'

