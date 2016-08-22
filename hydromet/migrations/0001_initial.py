# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlerteHydrometeorologique',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(blank=True, max_length=45)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('type_aggregation', models.CharField(default='sum', choices=[('sum', 'Somme'), ('avg', 'Moyenne'), ('count', 'Décompte'), ('max', 'Maximum'), ('min', 'Minimum')], null=True, max_length=5, blank=True)),
                ('type_comparaison', models.CharField(default='equal', choices=[('equal', 'Egal'), ('sup', 'Suppérieur'), ('sub', 'Inférieur')], null=True, max_length=5, blank=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Valeur', blank=True)),
                ('duree', models.PositiveSmallIntegerField(default=1, null=True, blank=True)),
                ('unite_duree', models.CharField(default='day', choices=[('hour', 'Heure'), ('day', 'Jour'), ('week', 'Semaine'), ('month', 'Mois'), ('year', 'Année')], null=True, max_length=5, blank=True)),
                ('niveau_alerte', models.CharField(default='jaune', choices=[('jaune', 'Jaune'), ('orange', 'Orange'), ('rouge', 'Rouge')], null=True, max_length=10, blank=True)),
                ('show_to_dashboard', models.BooleanField(default=True, verbose_name='Afficher sur le tableau de bord')),
                ('send_by_email', models.BooleanField(default=False, verbose_name='Envoyer par Email')),
                ('send_by_sms', models.BooleanField(default=False, verbose_name='Envoyer par SMS')),
                ('actif', models.BooleanField(default=True)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
                ('groupe', models.ForeignKey(null=True, to='auth.Group', blank=True, verbose_name='Groupe Concerné')),
            ],
            options={
                'verbose_name_plural': 'Alertes',
                'verbose_name': 'Alerte',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('time_result', models.DateTimeField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=15, verbose_name="Valeur de l'Observation", blank=True)),
                ('observateurhydromet', models.ForeignKey(null=True, to='base.Personne', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Log',
                'verbose_name': 'Log',
            },
        ),
        migrations.CreateModel(
            name='ObservateurHydromet',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('actif', models.BooleanField(default=True)),
                ('personne', models.OneToOneField(to='base.Personne')),
            ],
            options={
                'verbose_name_plural': 'Observateurs (Pluviométrique)',
                'verbose_name': 'Observateur (Pluviométrique)',
            },
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('time_start', models.DateTimeField(blank=True, null=True, verbose_name='Heure de Début')),
                ('time_end', models.DateTimeField(blank=True, null=True, verbose_name='Heure de Fin')),
                ('time_result', models.DateTimeField(verbose_name='Date')),
                ('duree', models.TimeField(help_text="Durée de l'évènemment en Heures:minutes:secondes", blank=True, null=True, verbose_name='Durée')),
                ('value', models.DecimalField(decimal_places=2, max_digits=15, verbose_name="Valeur de l'Observation", blank=True)),
                ('remarque', models.TextField(blank=True, max_length=100)),
                ('valider', models.BooleanField(default=False)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
                ('limite', models.ForeignKey(null=True, to='base.Limite', blank=True)),
                ('observateurhydromet', models.ForeignKey(null=True, to='hydromet.ObservateurHydromet', help_text="Laissez vide si l'observation provient d'une station automatique", blank=True, verbose_name='Observateurs')),
            ],
        ),
        migrations.CreateModel(
            name='Reseau',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(verbose_name='Description', max_length=100, blank=True)),
                ('institution_responsable', models.CharField(blank=True, max_length=100)),
                ('officiel', models.BooleanField(default=False, help_text="Cochez si ce réseau est reconnu officiellement par l'Etat Haitien.")),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Réseaux',
                'verbose_name': 'Réseau',
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('coordonnees_x_y', geoposition.fields.GeopositionField(blank=True, null=True, max_length=42, verbose_name='Position')),
                ('hauteur', models.DecimalField(default=0, decimal_places=2, max_digits=8, null=True, blank=True)),
                ('nom', models.CharField(verbose_name='Nom de la Station', max_length=45)),
                ('code', models.CharField(help_text='Le code est optionnel.', blank=True, null=True, max_length=45, verbose_name='Code de la Station')),
                ('description', models.TextField(blank=True, max_length=100)),
                ('actif', models.BooleanField(default=True)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
                ('limite', models.ForeignKey(null=True, to='base.Limite', blank=True, verbose_name='Zone')),
                ('reseau', models.ForeignKey(null=True, to='hydromet.Reseau', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeObservation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=45)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('max_value', models.DecimalField(decimal_places=2, blank=True, max_digits=15, null=True, verbose_name='Valeur Maximale Acceptée')),
                ('min_value', models.DecimalField(decimal_places=2, blank=True, max_digits=15, null=True, verbose_name='Valeur Minimale Acceptée')),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
                ('unitemesure', models.ForeignKey(null=True, to='base.UniteMesure', blank=True, verbose_name='Unite de mesure par défaut')),
            ],
            options={
                'verbose_name_plural': "Types d'Observation",
                'verbose_name': "Type d'Observations Hydrométéorologiques",
            },
        ),
        migrations.CreateModel(
            name='TypeStation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('marque', models.CharField(blank=True, max_length=100)),
                ('modele', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(verbose_name='Description', max_length=100, blank=True)),
                ('automatique', models.BooleanField(default=False, help_text='Cochez si ce modèle est un modèle automatique.')),
            ],
            options={
                'verbose_name_plural': 'Types de Station',
                'verbose_name': 'Type de Station',
            },
        ),
        migrations.CreateModel(
            name='TypeStationTypeObservation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('sos_standard', models.BooleanField(default=False, help_text='Cochez si le capteur répond au standard SOS.')),
                ('qualite', models.IntegerField(blank=True, validators=[django.core.validators.RegexValidator(regex='^[1-9][0-9]?$|^100$|^0$', message='Saisissez un nombre entre 0 et 100')], null=True, verbose_name='Qualité')),
                ('typeobservation', models.ForeignKey(to='hydromet.TypeObservation', verbose_name="Type d'Observation")),
                ('typestation', models.ForeignKey(to='hydromet.TypeStation')),
                ('unitemesure', models.ForeignKey(null=True, to='base.UniteMesure', blank=True, verbose_name='Unité de mesure pour cette station')),
            ],
            options={
                'verbose_name_plural': "Types d'Observations Hydrométéorologiques",
                'verbose_name': "Type d'Observations Hydrométéorologiques",
            },
        ),
        migrations.AddField(
            model_name='station',
            name='typestation',
            field=models.ForeignKey(null=True, to='hydromet.TypeStation', blank=True, verbose_name='Type de la Station'),
        ),
        migrations.AddField(
            model_name='observation',
            name='station',
            field=models.ForeignKey(to='hydromet.Station'),
        ),
        migrations.AddField(
            model_name='observation',
            name='typeobservation',
            field=models.ForeignKey(null=True, to='hydromet.TypeObservation', blank=True, verbose_name="Type de l'Observation"),
        ),
        migrations.AddField(
            model_name='observateurhydromet',
            name='station',
            field=models.ForeignKey(to='hydromet.Station'),
        ),
        migrations.AddField(
            model_name='log',
            name='observation',
            field=models.ForeignKey(null=True, default=None, to='hydromet.Observation'),
        ),
        migrations.AddField(
            model_name='alertehydrometeorologique',
            name='station',
            field=models.ForeignKey(null=True, to='hydromet.Station', blank=True),
        ),
        migrations.AddField(
            model_name='alertehydrometeorologique',
            name='typeobservation',
            field=models.ForeignKey(null=True, to='hydromet.TypeObservation', blank=True, verbose_name="Type de l'Observation"),
        ),
        migrations.AlterUniqueTogether(
            name='typestationtypeobservation',
            unique_together=set([('typestation', 'typeobservation')]),
        ),
        migrations.AlterUniqueTogether(
            name='observateurhydromet',
            unique_together=set([('station', 'personne')]),
        ),
    ]
