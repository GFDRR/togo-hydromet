from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import *
from rapidsms.backends.kannel.views import KannelBackendView


urlpatterns = [
    url(r'^', include('public.urls', 'public')),
    url(r'^hydromet/', include('hydromet.urls', 'hydromet')),

    url(r'^admin/$', 'togohydromet.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/hydromet/rapport/$', 'hydromet.views.rapport'),



    # RapidSMS base URLs
    url(r'^accounts/', include('rapidsms.urls.login_logout')),
    url(r'^rapidsms/$', 'rapidsms.views.dashboard', name='rapidsms-dashboard'),

    # RapidSMS contrib app URLs
    url(r'^httptester/', include('rapidsms.contrib.httptester.urls')),
    url(r'^messagelog/', include('rapidsms.contrib.messagelog.urls')),
    url(r'^messaging/', include('rapidsms.contrib.messaging.urls')),
    url(r'^registration/', include('rapidsms.contrib.registration.urls')),
    url(r'^backend/kannel-fake-smsc/$',KannelBackendView.as_view(backend_name='kannel-fake-smsc')),

    # Third party URLs
    url(r'^selectable/', include('selectable.urls')),
    url(r'^backend/kannel-usb0-smsc/$', KannelBackendView.as_view(backend_name='kannel-usb0-smsc')),
    url(r'^select2/', include('django_select2.urls')),

    # API
    url(r'^api/v1/', include('api.urls', 'api')),


    # SMS Lapli URLs
    #url(r'^rapport/pluviometrie/$','public.views.rpluie'),
    #url(r'^rapport/json_rap/', 'public.views.json_rap'),
    #url(r'^rapport/json_graph/', 'public.views.json_graph'),
    #url(r'^rapport/json_map/$', 'public.views.json_map'),
    #url(r'^rapport/average/$', 'public.views.json_average_by_dep'),
    #url(r'^rapport/pluviometrie/station_map/$', 'public.views.station_map'),
    #url(r'^rapport/pluviometrie/comp/$', 'public.views.compBDep'),

    url(r'^test', 'public.views.imp'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
