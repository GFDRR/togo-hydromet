# -*- coding: utf-8 -*-
from django.contrib.gis import admin

# Register your models here.
from hydromet.models import TypeStationTypeObservation, TypeStation, ObservateurHydromet, Observation, TypeObservation, Station, Log, AlerteHydrometeorologique, Reseau
from base.models import Limite
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from easy_select2 import select2_modelform

from django.forms import ModelForm
from suit.widgets import LinkedSelect, SuitSplitDateTimeWidget


StationForm = select2_modelform(Station, attrs={'width': '250px'})

ObservationForm = select2_modelform(Observation, attrs={'width': '250px'})



#class ObservationForm(ModelForm):
    #class Meta:
        #select2_modelform(Observation, attrs={'width': '250px'})
        #widgets = {
            #'time_start': SuitSplitDateTimeWidget,
            #'time_end': SuitSplitDateTimeWidget,
            #'time_result': SuitSplitDateTimeWidget,
        #}




def validate(modeladmin, request, queryset):
    queryset.update(valider=True)
validate.short_description = "Valider les observations selectionnées"


def unvalidate(modeladmin, request, queryset):
    queryset.update(valider=False)
unvalidate.short_description = "Invalider les observations selectionnées"


class TypeStationTypeObservationInline(admin.TabularInline):
    model = TypeStationTypeObservation
    extra = 2

class StationResource(resources.ModelResource):
    class Meta:
        model = Station
        exclude = ('timestamp_add', )

class TypeStationAdmin(admin.ModelAdmin):
    inlines = [TypeStationTypeObservationInline]


class StationAdmin(ImportExportModelAdmin):
    list_display = ("nom", "typestation" ,"limite", "actif")
    list_filter = ('actif',)
    search_fields = ["nom"]
    exclude = ('timestamp_add', )
    form = StationForm
    resources = StationResource


class ObservateurAdmin(admin.ModelAdmin):
    list_display = ("station", "personne")


class ObservationAdmin(ImportExportModelAdmin):

    def log_count(self, obj):
        return obj.log_set.count()
    log_count.short_description = "Log"

    def val_unite(self, obj):
        #return "%s %s" % (obj.value,  obj.typeobservation.unitemesure.unite)
        return "%s" % (obj.value)
    val_unite.short_description = "Value"

    list_display = ("station", "typeobservation", "val_unite", "time_result", "remarque", "log_count", "valider")
    list_filter = ('limite', 'time_result',)
    search_fields = ["station__nom", "time_result"]
    actions = [validate, unvalidate]
    form = ObservationForm


class LogAdmin(admin.ModelAdmin):
    list_display = ("observation", "observateurhydromet", "contact", "time_result", "value")
    list_filter = ('time_result', 'observation')
    # search_fields = ["nom"]


class TypeObservationAdmin(admin.ModelAdmin):
    list_display = ("nom", "unitemesure")
    search_fields = ["nom"]


# Added all in the register
admin.site.register(Station, StationAdmin)
admin.site.register(TypeStation, TypeStationAdmin)
admin.site.register(Observation, ObservationAdmin)
admin.site.register(ObservateurHydromet, ObservateurAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(TypeObservation, TypeObservationAdmin)
admin.site.register(AlerteHydrometeorologique)
admin.site.register(Reseau)