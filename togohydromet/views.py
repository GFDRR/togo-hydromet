from django.db.models import Count
from django.shortcuts import render
from base.models import Limite
from hydromet.models import Station, ObservateurHydromet, Observation, TypeObservation
from django.contrib.auth.models import User
import datetime

# Create your views here.

def home(request):
    observateur_all = ObservateurHydromet.objects.all();
    # for observation in Observation.objects.filer(time_result):
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

    return render(request, "admin/index.html", {
        'menu_active':'accueil',
        'station_qt': Station.objects.count(),
        'observers_qt': ObservateurHydromet.objects.count(),
        'prefectures_qt': Limite.objects.filter(typelimite__niveau=2).count(),
        'users_qt': User.objects.count(),
        'observers_check_qt': Observation.objects.filter(time_result__range=(today_min, today_max)).values("observateurhydromet").annotate(Count("id")).order_by().count(),
        'observers_warning_qt': ObservateurHydromet.objects.all().count(),
        'observers_error_qt': Observation.objects.count(),
    })

