# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Limite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=40)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('temp', models.BooleanField(default=True)),
                ('code', models.CharField(blank=True, max_length=20)),
                ('type', models.CharField(blank=True, null=True, max_length=2, choices=[('rural', 'Rural'), ('urbain', 'Urbain')])),
                ('shape', django.contrib.gis.db.models.fields.PolygonField(srid=4326, blank=True, null=True)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Limites Administratives',
                'verbose_name': 'Limite Administrative',
            },
        ),
        migrations.CreateModel(
            name='Observatoire',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(blank=True, max_length=40)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('actif', models.BooleanField(default=True)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
                ('limite', models.ForeignKey(to='base.Limite', verbose_name='Département')),
            ],
        ),
        migrations.CreateModel(
            name='ObservatoireLimite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
                ('limite', models.ForeignKey(to='base.Limite')),
                ('observatoire', models.ForeignKey(to='base.Observatoire')),
            ],
            options={
                'verbose_name_plural': "Limites couvert par l'Observatoire",
                'verbose_name': 'Limite',
            },
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=45)),
                ('prenom', models.CharField(max_length=45)),
                ('telephone_bureau', models.CharField(verbose_name='Telephone (Bureau)', validators=[django.core.validators.RegexValidator(regex='^509[0-9]{8}$', message="La valeur ne correspond pas au format d'un numero de telephone")], max_length=45)),
                ('telephone_personnel', models.CharField(verbose_name='Telephone (Personnel)', blank=True, validators=[django.core.validators.RegexValidator(regex='^509[0-9]{8}$', message="La valeur ne correspond pas au format d'un numero de telephone")], max_length=45)),
                ('email', models.CharField(blank=True, max_length=45)),
                ('adresse', models.TextField(blank=True, max_length=100)),
                ('no_id', models.CharField(verbose_name='NIF/CIN', validators=[django.core.validators.RegexValidator(regex='^[0-9]{3}-[0-9]{3}-[0-9]{3}-[0-9]{1}$|^\\d{2}-\\d{2}-\\d{2}-\\d{4}-\\d{2}-\\d{5}$', message="La valeur ne correspond ni au formt d'un code CIN ni a celui d'un NIF")], max_length=45, unique=True)),
                ('date_embauche', models.DateField(verbose_name="Date d'embauche")),
                ('note', models.TextField(blank=True, max_length=200)),
                ('actif', models.BooleanField()),
                ('observatoire', models.ForeignKey(to='base.Observatoire', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Poste',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nom_poste', models.CharField(max_length=45)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeLimite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=40)),
                ('niveau', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeZone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=40)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UniteMesure',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=45)),
                ('unite', models.CharField(max_length=7, unique=True)),
                ('description', models.TextField(blank=True)),
                ('formule', models.DecimalField(decimal_places=3, blank=True, null=True, verbose_name='Formule', max_digits=5)),
            ],
            options={
                'verbose_name_plural': 'Unités de Mesure',
                'verbose_name': 'Unité de Mesure',
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=40)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('shape', django.contrib.gis.db.models.fields.PolygonField(srid=4326, blank=True, null=True)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
                ('typezone', models.ForeignKey(to='base.TypeZone', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Zones Personnalisées',
                'verbose_name': 'Zone Personnalisée',
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
            field=models.ForeignKey(to='base.TypeLimite', verbose_name='Niveau'),
        ),
        migrations.AlterUniqueTogether(
            name='observatoirelimite',
            unique_together=set([('observatoire', 'limite')]),
        ),
    ]
