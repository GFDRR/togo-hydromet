__author__ = 'jbjeanniton'

from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from hydromet.models import Observation, AlerteHydrometeorologique


@receiver(post_save, sender=Observation)
def station_post_save(sender, **kwargs):
    # Gestion des alertes
    alertes_lst = AlerteHydrometeorologique.objects.filter(actif=True)
