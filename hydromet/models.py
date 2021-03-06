from togohydromet.regex import regex_percent
from django.contrib.gis.db import models
from base.models import Personne, Limite, UniteMesure
from django.contrib.auth.models import Group
from geoposition.fields import GeopositionField
from django.core import serializers


#  -------------------------------------------
#  Models for Hm
#  -------------------------------------------


class TypeStation(models.Model):
    marque = models.CharField(max_length=100, blank=True)
    modele = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=100, blank=True, verbose_name="Description")
    automatique = models.BooleanField(default=False, help_text="Cochez si ce modèle est un modèle automatique.")

    class Meta:
        verbose_name = "Type de Station"
        verbose_name_plural = "Types de Station"

    def __str__(self):  # __unicode__ on Python 2
        return "%s, %s" % (self.marque, self.modele)


class Reseau(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(max_length=100, blank=True, verbose_name="Description")
    institution_responsable = models.CharField(max_length=100, blank=True)
    officiel = models.BooleanField(default=False, help_text="Cochez si ce réseau est reconnu officiellement par l'Etat Haitien.")
    timestamp_add = models.DateTimeField(auto_now_add=True)
    timestamp_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Réseau"
        verbose_name_plural = "Réseaux"

    def __str__(self):  # __unicode__ on Python 2
        return "%s" % (self.nom)


class Station(models.Model):
    reseau = models.ForeignKey(Reseau, null=True, blank=True)
    limite = models.ForeignKey(Limite, null=True, blank=True, verbose_name="Zone",)
    coordonnees_x_y = models.PointField(null=True, blank=True, verbose_name="Position (Latitude, Logitude)")
    elevation = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True, null=True)
    nom = models.CharField(max_length=45, verbose_name="Nom de la Station")
    code = models.CharField(max_length=45, verbose_name="Code de la Station", null=True, blank=True,
                            help_text="Le code est optionnel.")
    typestation = models.ForeignKey(TypeStation, verbose_name="Type de la Station", null=True, blank=True)
    description = models.TextField(max_length=100, blank=True)
    actif = models.BooleanField(default=True)
    timestamp_add = models.DateTimeField(auto_now_add=True)
    timestamp_update = models.DateTimeField(auto_now=True)
    objects = models.GeoManager()

    @property
    def type_limite(self): # __unicode__ on Python 2
        return self.limite.typelimite.nom

    @property
    def nom_limite(self):  # __unicode__ on Python 2
        return self.limite.nom

    @property
    def nom_reseau(self):  # __unicode__ on Python 2
        return self.reseau.nom

    @property
    def nom_typestation(self):  # __unicode__ on Python 2
        return self.typestation.marque

    @property
    def type_observation(self):
        list_type_observations = []
        for type_obs_type_st in self.typestation.typestationtypeobservation_set.all():
            list_type_observations.append({
                'type': type_obs_type_st.typeobservation.nom,
                'unite': type_obs_type_st.unitemesure.nom,
                'sos_standard': type_obs_type_st.sos_standard,
                'qualite': type_obs_type_st.qualite,
            })

        return list_type_observations

    def __str__(self):  # __unicode__ on Python 2
        return self.nom


class ObservateurHydromet(models.Model):
    station = models.ForeignKey(Station)
    personne = models.OneToOneField(Personne)
    actif = models.BooleanField(default=True)

    class Meta:
        #unique_together = ('station', 'personne')
        verbose_name = "Observateur"
        verbose_name_plural = "Observateurs"

    def __str__(self):  # __unicode__ on Python 2
        return "%s : %s " % (self.personne, self.station)


class CategorieTypeObservation(models.Model):
    nom = models.CharField(max_length=45)
    description = models.TextField(max_length=100, blank=True)
    timestamp_add = models.DateTimeField(auto_now_add=True)
    timestamp_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Catégorie des Types d'Observations"
        verbose_name_plural = "Catégories des Types d'Observation"

    def __str__(self):  # __unicode__ on Python 2
        return "%s" % self.nom


class TypeObservation(models.Model):
    categorietypeobservation = models.ForeignKey(CategorieTypeObservation, null=True,  default=None, verbose_name="Catégorie");
    nom = models.CharField(max_length=45)
    unitemesure = models.ForeignKey(UniteMesure, verbose_name="Unite de mesure par défaut", null=True, blank=True)
    description = models.TextField(max_length=100, blank=True)
    code = models.CharField(max_length=45, verbose_name="Code du Type d'Obeservation", null=True, blank=True,
                            help_text="Le code est optionnel. Optez de préférence pour une lettre.")
    max_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                    verbose_name="Valeur Maximale Acceptée")
    min_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                    verbose_name="Valeur Minimale Acceptée")
    timestamp_add = models.DateTimeField(auto_now_add=True)
    timestamp_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Type d'Observations"
        verbose_name_plural = "Types d'Observation"

    def __str__(self):  # __unicode__ on Python 2
        return "%s" % self.nom


class TypeStationTypeObservation(models.Model):
    typestation = models.ForeignKey(TypeStation)
    typeobservation = models.ForeignKey(TypeObservation, verbose_name="Type d'Observation")
    unitemesure = models.ForeignKey(UniteMesure, verbose_name="Unité de mesure pour cette station", null=True, blank=True)
    sos_standard = models.BooleanField(default=False, help_text="Cochez si le capteur répond au standard SOS.")
    qualite = models.IntegerField(blank=True, null=True, verbose_name="Qualité", validators=[
        regex_percent,
    ])

    class Meta:
        verbose_name = "Type d'Observations Hydrométéorologiques"
        verbose_name_plural = "Types d'Observations Hydrométéorologiques"
        unique_together = ('typestation', 'typeobservation',)

    @property
    def nom_typeobservation(self):  # __unicode__ on Python 2
        return "%s" % "s"

    def __str__(self):  # __unicode__ on Python 2
        return "%s" % self.unitemesure


class Observation(models.Model):
    station = models.ForeignKey(Station)
    observateurhydromet = models.ForeignKey(ObservateurHydromet, null=True, blank=True, verbose_name="Observateurs", help_text="Laissez vide si l'observation provient d'une station automatique")
    limite = models.ForeignKey(Limite, null=True, blank=True)
    typeobservation = models.ForeignKey(TypeObservation, verbose_name="Type de l'Observation", null=True, blank=True)
    time_start = models.DateTimeField(verbose_name="Heure de Début", null=True, blank=True)
    time_end = models.DateTimeField(verbose_name="Heure de Fin", null=True, blank=True)
    time_result = models.DateTimeField(verbose_name="Date")
    duree = models.TimeField(verbose_name="Durée", null=True, blank=True, help_text="Durée de l'évènemment en Heures:minutes:secondes")
    value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, verbose_name="Valeur de l'Observation")
    remarque = models.TextField(max_length=100, blank=True)
    valider = models.BooleanField(default=False)
    timestamp_add = models.DateTimeField(auto_now_add=True)
    timestamp_update = models.DateTimeField(auto_now=True)

    @property
    def code_departement(self):
        return self.code[:2]

    @property
    def nom_typeobservation(self):
        return self.typeobservation.nom

    @property
    def unite_typeobservation(self):
        return self.typeobservation.unitemesure.nom

    def __str__(self):  # __unicode__ on Python 2
        return "%s : %s" % (self.time_result, self.value)


class Log(models.Model):
    observation = models.ForeignKey(Observation, null=True, default=None)
    observateurhydromet = models.ForeignKey(Personne, null=True, blank=True)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    time_result = models.DateTimeField()
    value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, verbose_name="Valeur de l'Observation")

    @property
    def contact(self):
        if self.observateurhydromet:
            return "%s, %s" % (self.observateurhydromet.telephone_bureau, self.observateurhydromet.email)
        else:
            return "N/A"

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Log"

    def __str__(self):  # __unicode__ on Python 2
        return "%s, par %s " % (self.observation, self.observateurhydromet.nom if self.observateurhydromet else "N/A" )


class AlerteHydrometeorologique(models.Model):
    SUM = 'sum'
    AVG = 'avg'
    COUNT = 'count'
    MAX = 'max'
    MIN = 'min'
    TYPE_AGG = (
        (SUM, 'Somme'),
        (AVG, 'Moyenne'),
        (COUNT, 'Décompte'),
        (MAX, 'Maximum'),
        (MIN, 'Minimum'),
    )

    EQUAL = 'equal'
    SUP = 'sup'
    SUB = 'sub'
    TYPE_COMP = (
        (EQUAL, 'Egal'),
        (SUP, 'Suppérieur'),
        (SUB, 'Inférieur'),
    )

    HOUR = 'hour'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'
    UNITE_DUREE = (
        (HOUR, 'Heure'),
        (DAY, 'Jour'),
        (WEEK, 'Semaine'),
        (MONTH, 'Mois'),
        (YEAR, 'Année'),
    )

    JAUNE = 'jaune'
    ORANGE = 'orange'
    ROUGE = 'rouge'
    NIVEAU_ALERTE = (
        (JAUNE, 'Jaune'),
        (ORANGE, 'Orange'),
        (ROUGE, 'Rouge'),
    )

    nom = models.CharField(max_length=45, blank=True)
    description = models.TextField(max_length=100, blank=True)
    station = models.ForeignKey(Station, null=True, blank=True)
    typeobservation = models.ForeignKey(TypeObservation, verbose_name="Type de l'Observation", null=True, blank=True)
    type_aggregation = models.CharField(max_length=5, choices=TYPE_AGG, null=True, blank=True, default=SUM)
    type_comparaison = models.CharField(max_length=5, choices=TYPE_COMP, null=True, blank=True, default=EQUAL)
    value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, verbose_name="Valeur")
    duree = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    unite_duree = models.CharField(max_length=5, choices=UNITE_DUREE, null=True, blank=True, default=DAY)
    niveau_alerte = models.CharField(max_length=10, choices=NIVEAU_ALERTE, null=True, blank=True, default=JAUNE)
    show_to_dashboard = models.BooleanField(default=True, verbose_name="Afficher sur le tableau de bord")
    send_by_email = models.BooleanField(default=False, verbose_name="Envoyer par Email")
    send_by_sms = models.BooleanField(default=False, verbose_name="Envoyer par SMS")
    groupe = models.ForeignKey(Group, verbose_name="Groupe Concerné", null=True, blank=True)
    actif = models.BooleanField(default=True)
    timestamp_add = models.DateTimeField(auto_now_add=True)
    timestamp_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Alerte"
        verbose_name_plural = "Alertes"

    def __str__(self):  # __unicode__ on Python 2
        return "%s" % (self.nom)
