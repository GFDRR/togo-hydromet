from datetime import timedelta, datetime
import time
from django.shortcuts import render
from django.http import JsonResponse

from django.utils import formats
from django.db.models import Q
from django.db.models import Avg, Sum, Min, Max
from django.db import connection

from base.models import Limite
from hydromet.models import Station, Observation, TypeObservation

from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt


def local_to_utc(t):
    """Make sure that the dst flag is -1 -- this tells mktime to take daylight
    savings into account"""
    secs = time.mktime(t)
    return time.gmtime(secs)


def map_overview(request):
    dept_lst = request.POST.getlist('sel_dept[]')

    stations_list = []
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    for station in Station.objects.filter(Q(limite__pk__in=dept_lst) | Q(limite__isnull=True)).exclude(
            coordonnees_x_y='None'):
        observation = Observation.objects.filter(station=station, valider=request.user.is_authenticated()).order_by('-pk').first()
        if not observation:
            quantite_pluie = '-'
            statut = 'no_activity'
            date_update = ''
        else:
            quantite_pluie = observation.value
            statut = 'high_activity'
            date_update = datetime.combine(observation.time_result, datetime.min.time())

        if date_update and date_update >= today:
            statut = 'high_activity'
        elif date_update and date_update < today and date_update >= today - timedelta(days=7):
            statut = 'low_activity'
        elif date_update:
            statut = 'no_activity'

        if not station.actif:
            statut = 'off_activity'

        format_date = formats.date_format(date_update, "SHORT_DATE_FORMAT") if date_update else '--'

        # typeObs = TypeStationTypeObservation.objects.filter(typestation=station.typestation)

        # if typeObs:
        # for type in typeObs:
        # print(type.typeobservation.nom.encode('utf-8'))

        # unite = observation.typeobservation.unitemesure
        # if not unite:
        # unite = 'N/A'
        latitude = ''
        longitude = ''
        if station.coordonnees_x_y:
            latitude = station.coordonnees_x_y.latitude
            longitude = station.coordonnees_x_y.longitude

        stations_list.append(
            {'nomStation': station.nom, 'latitude': latitude, 'longitude': longitude,
             'qt': quantite_pluie, 'statut': statut, 'dateUpdate': format_date, 'today': today})

    return JsonResponse({'stations_lst': stations_list})


def chart_overview(request):
    today = datetime.now();
    dept_lst = []
    sel_duree = "%s - %s" % (datetime.strftime(today-timedelta(days=365), '%d/%m/%Y'), datetime.strftime(today, '%d/%m/%Y'))
    sel_type_aggr = 'Sum'
    sel_type_duree = 'month'
    sel_type_observation = '1'
    filter_dept = {}

    if request.POST:
        dept_lst = request.POST.getlist('sel_dept[]')
        sel_duree = request.POST.get('sel_duree')
        sel_type_aggr = request.POST.get('sel_type_aggr')
        sel_type_duree = request.POST.get('sel_type_duree')
        sel_type_observation = request.POST.get('sel_type_observation')
        filter_dept['pk__in'] = dept_lst

    filter_date = {}
    if sel_duree :
        date_interval = sel_duree.split(' - ')
        if date_interval[0]:
            filter_date['time_result__gte'] = datetime.strptime(date_interval[0], '%d/%m/%Y')

        if date_interval[1]:
            filter_date['time_result__lte'] = datetime.strptime(date_interval[1], '%d/%m/%Y')

    result_set = {}

    aggr_eval = sel_type_aggr+"('value')"

    for limite in Limite.objects.filter(typelimite__niveau=1, **filter_dept):
        result_set[limite.nom] = []
        truncate_date = connection.ops.date_trunc_sql(sel_type_duree, 'time_result')
        observations = Observation.objects.extra(select={sel_type_duree:truncate_date})\
            .filter(limite__code__startswith=limite.code, typeobservation__pk=sel_type_observation, **filter_date).values(sel_type_duree).annotate(eval(aggr_eval))
        for observation in observations:
            result_set[limite.nom].append({'date': observation[sel_type_duree], 'value': format(observation['value__'+sel_type_aggr.lower()], '.2f')})

    return JsonResponse({'dept_lst': result_set})

@csrf_exempt
def rapport(request):
    departement_lst = Limite.objects.filter(typelimite__niveau=1)
    type_observation_lst = TypeObservation.objects.all()
    month_lst = []
    selDate = datetime.today()

    for x in range(0, 12):
        first = selDate.replace(day=1)
        last_month = first - timedelta(days=1)
        month_lst.append({'key': last_month.strftime("%Y-%m-01"), 'val': last_month.strftime("%B %Y")})
        selDate = last_month

    return render(request, "hydromet/rapport.html", {'dep_lst': departement_lst, 'type_obs_lst': type_observation_lst, 'month_lst': month_lst, })

