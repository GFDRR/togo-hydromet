__author__ = 'rpalexis'
from django.conf.urls import include, url, patterns
from django.contrib import admin
urlpatterns = patterns('public.views',
    url(r'^$', 'home'),
    url(r'^accueil/$', 'home'),
    url(r'^faq/$', 'faq'),
    url(r'rapport/pluviometrie/$', 'pluviometrie'),
    url(r'rapport/prix_marche/$', 'prix_marche'),
    url(r'rapport/pluviometrie/overview/$', 'pluviometrie'),
)
