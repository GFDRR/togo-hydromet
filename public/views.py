from django.shortcuts import render
from base.models import Limite
from hydromet.models import Observation, TypeObservation
import datetime

# Create your views here.

def home(request):
    return render(request, "public/index.html", {'menu_active':'accueil'})


def faq(request):
    return render(request, "public/faq.html", {'menu_active':'faq'})


def pluviometrie(request):
    departement_lst = Limite.objects.filter(typelimite__niveau='1')
    type_observation_lst = TypeObservation.objects.all()
    month_lst = []
    selDate = datetime.date.today()

    for x in range(0,12):
        first = selDate.replace(day=1)
        last_month = first - datetime.timedelta(days=1)
        month_lst.append({'key': last_month.strftime("%Y-%m-01"), 'val': last_month.strftime("%B %Y")})
        selDate = last_month

    return render(request, "public/pluviometrie.html", {'menu_active': 'pluviometrie', 'type_obs_lst': type_observation_lst, 'dep_lst': departement_lst, 'month_lst': month_lst })


def prix_marche(request):
    departement_lst = Limite.objects.filter(typelimite__nom='Département')
    type_observation_lst = TypeObservation.objects.all()
    month_lst = []
    selDate = datetime.date.today()

    for x in range(0,12):
        first = selDate.replace(day=1)
        last_month = first - datetime.timedelta(days=1)
        month_lst.append({'key': last_month.strftime("%Y-%m-01"), 'val': last_month.strftime("%B %Y")})
        selDate = last_month

    return render(request, "public/prix_marche.html", {'menu_active': 'marche', 'type_obs_lst': type_observation_lst, 'dep_lst': departement_lst, 'month_lst': month_lst })


def imp(request):
    recupAll = Observation.objects.select_related('idStation')
    dd = []
    for e in recupAll:
        dd.append(e)
    return render(request, "public/test.html", {'val': dd})





