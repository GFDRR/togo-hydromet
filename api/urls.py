__author__ = 'jbjeanniton'

from django.conf.urls import include, url, patterns
from api import views

urlpatterns = patterns('api.views',
                       url(r'^stations/$', 'stations_list'),
                       url(r'^stations/(?P<id_station>[0-9]{0,4})$', 'station_info'),

                       url(r'^stations/(?P<id_station>[0-9]{0,4})/observations/$', 'station_observations'),
                       url(r'^stations/(?P<id_station>[0-9]{0,4})/observations/(?P<year>[0-9]{0,4})/$',
                           'station_observations'),
                       url(r'^stations/(?P<id_station>[0-9]{0,4})/observations/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$'
                           , 'station_observations'),
                       url(r'^stations/(?P<id_station>[0-9]{0,4})/observations/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})'
                           r'/(?P<day>[0-9]{2})/$', 'station_observations'),

                       url(r'^observations/$', 'all_observations'),
                       url(r'^observations/(?P<year>[0-9]{4})/$', 'all_observations'),
                       url(r'^observations/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', 'all_observations'),
                       url(r'^observations/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',
                           'all_observations'),
                       )
