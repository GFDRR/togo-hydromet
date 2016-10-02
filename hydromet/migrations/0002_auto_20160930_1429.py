# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hydromet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorieTypeObservation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nom', models.CharField(max_length=45)),
                ('description', models.TextField(max_length=100, blank=True)),
                ('timestamp_add', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': "Catégories des Types d'Observation",
                'verbose_name': "Catégorie des Types d'Observations",
            },
        ),
        migrations.AlterModelOptions(
            name='observateurhydromet',
            options={'verbose_name_plural': 'Observateurs', 'verbose_name': 'Observateur'},
        ),
        migrations.AlterModelOptions(
            name='typeobservation',
            options={'verbose_name_plural': "Types d'Observation", 'verbose_name': "Type d'Observations"},
        ),
        migrations.AlterUniqueTogether(
            name='observateurhydromet',
            unique_together=set([]),
        ),
        migrations.AddField(
            model_name='typeobservation',
            name='categorietypeobservation',
            field=models.ForeignKey(default=None, null=True, to='hydromet.CategorieTypeObservation'),
        ),
    ]
