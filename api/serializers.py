from hydromet.models import Station, Reseau, Observation
from rest_framework import serializers


class ReseauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reseau
        fields = ('nom')


class AllStationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ('pk', 'nom', 'code', 'nom_limite', 'coordonnees_x_y', 'description')


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        depth = 1
        fields = (
            'pk', 'nom', 'code', 'nom_limite', 'type_limite', 'coordonnees_x_y', 'nom_reseau', 'description',
            'typestation',
            'type_observation')


class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = ('value', 'typeobservation', 'time_result', 'nom_typeobservation', 'unite_typeobservation')
