from django.shortcuts import render

from hydromet.models import Station, Reseau, Observation
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from api.serializers import AllStationsSerializer, StationSerializer, ObservationSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def stations_list(request):
    if request.method == 'GET':
        stations = Station.objects.all()
        serializer = AllStationsSerializer(stations, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def station_info(request, id_station="0"):
    if request.method == 'GET':
        station = Station.objects.filter(code=id_station).first()
        serializer = StationSerializer(station)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def station_observations(request, id_station="0", year="([0-9]{4})", month="([0-9]{2})", day="([0-9]{2})"):
    if request.method == 'GET':
        station = Station.objects.filter(code=id_station).first()
        observations = Observation.objects.filter(station=station, valider=True,
                                                  time_result__regex=r'' + year + '-' + month + '-' + day)
        serializer = ObservationSerializer(observations, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def all_observations(request, year="([0-9]{4})", month="([0-9]{2})", day="([0-9]{2})", start_date="", end_date=""):
    if request.method == 'GET':
        # parameters : start_date; end_date; type_observation; aggregation;
        observations = Observation.objects.filter(valider=True, time_result__regex=r'' + year + '-' + month + '-' + day,
                                                  time_result__range=(start_date +' 01:00', end_date +' 01:00'))
        serializer = ObservationSerializer(observations, many=True)
        return Response(serializer.data)
