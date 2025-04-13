import os
import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings
from arches.app.models.models import MapLayer

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        try:
            streets = MapLayer.objects.get(name="streets")
            satellite = MapLayer.objects.get(name="satellite")
            outdoor = MapLayer.objects.get(name="LCAI-Outdoor")
            lcai = MapLayer.objects.get(name="Outdoors")
        except MapLayer.DoesNotExist:
            print("can't find expected maplayer")
            return

        streets.addtomap = False
        streets.name = "Streets"
        streets.save()

        satellite.name = "Satellite"
        satellite.save()

        outdoor.activated = False
        outdoor.save()

        lcai.addtomap = True
        lcai.save()
