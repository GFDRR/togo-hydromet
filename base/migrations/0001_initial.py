# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Limite',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=40)),
                ('description', models.TextField(max_length=100, blank=True)),
                ('temp', models.BooleanField(default=True)),
                ('code', models.CharField(max_length=20, blank=True)),
                ('type', models.CharField(max_length=2, null=True, choices=[('rural', 'Rural'), ('urbain', 'Urbain')], blank=True)),
                ('shape', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=4326, blank=True)),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326, blank=True)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Limite Administrative',
                'verbose_name_plural': 'Limites Administratives',
            },
        ),
        migrations.CreateModel(
            name='Observatoire',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=40, blank=True)),
                ('description', models.TextField(max_length=100, blank=True)),
                ('actif', models.BooleanField(default=True)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
                ('limite', models.ForeignKey(verbose_name='Département', to='base.Limite')),
            ],
        ),
        migrations.CreateModel(
            name='ObservatoireLimite',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
                ('limite', models.ForeignKey(to='base.Limite')),
                ('observatoire', models.ForeignKey(to='base.Observatoire')),
            ],
            options={
                'verbose_name': 'Limite',
                'verbose_name_plural': "Limites couvert par l'Observatoire",
            },
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=45)),
                ('prenom', models.CharField(max_length=45)),
                ('telephone_bureau', models.CharField(max_length=45, verbose_name='Telephone (Bureau)', validators=[django.core.validators.RegexValidator(message="La valeur ne correspond pas au format d'un numero de telephone", regex='^509[0-9]{8}$')])),
                ('telephone_personnel', models.CharField(max_length=45, verbose_name='Telephone (Personnel)', blank=True, validators=[django.core.validators.RegexValidator(message="La valeur ne correspond pas au format d'un numero de telephone", regex='^509[0-9]{8}$')])),
                ('email', models.CharField(max_length=45, blank=True)),
                ('adresse', models.TextField(max_length=100, blank=True)),
                ('no_id', models.CharField(max_length=45, verbose_name='NIF/CIN', validators=[django.core.validators.RegexValidator(message="La valeur ne correspond ni au formt d'un code CIN ni a celui d'un NIF", regex='^[0-9]{3}-[0-9]{3}-[0-9]{3}-[0-9]{1}$|^\\d{2}-\\d{2}-\\d{2}-\\d{4}-\\d{2}-\\d{5}$')], unique=True)),
                ('date_embauche', models.DateField(verbose_name="Date d'embauche")),
                ('note', models.TextField(max_length=200, blank=True)),
                ('actif', models.BooleanField()),
                ('observatoire', models.ForeignKey(null=True, to='base.Observatoire', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Poste',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nom_poste', models.CharField(max_length=45)),
                ('description', models.TextField(max_length=100, blank=True)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeLimite',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=40)),
                ('niveau', models.IntegerField(default=0)),
                ('description', models.TextField(max_length=100, blank=True)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeZone',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=40)),
                ('description', models.TextField(max_length=100, blank=True)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UniteMesure',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=45)),
                ('unite', models.CharField(max_length=7, unique=True)),
                ('description', models.TextField(blank=True)),
                ('formule', models.DecimalField(decimal_places=3, verbose_name='Formule', max_digits=5, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Unité de Mesure',
                'verbose_name_plural': 'Unités de Mesure',
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=40)),
                ('description', models.TextField(max_length=100, blank=True)),
                ('shape', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=4326, blank=True)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
                ('typezone', models.ForeignKey(null=True, to='base.TypeZone', blank=True)),
            ],
            options={
                'verbose_name': 'Zone Personnalisée',
                'verbose_name_plural': 'Zones Personnalisées',
            },
        ),
        migrations.AddField(
            model_name='personne',
            name='poste',
            field=models.ForeignKey(to='base.Poste'),
        ),
        migrations.AddField(
            model_name='limite',
            name='typelimite',
            field=models.ForeignKey(verbose_name='Niveau', to='base.TypeLimite'),
        ),
        migrations.AlterUniqueTogether(
            name='observatoirelimite',
            unique_together=set([('observatoire', 'limite')]),
        ),
    ]
