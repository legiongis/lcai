import os
import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from arches.app.models.resource import Resource
from arches.app.models.models import ResourceInstance

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        graph_names = [
            "3D Rock Art Panel",
            "Document",
            "Image",
        ]

        for g in graph_names:
            print(g)
            instances = Resource.objects.filter(graph__name=g)
            print(instances.count())
            header = ["resourceinstanceid", "title"]
            rows = [header]
            for res in instances:
                row = [str(res.pk), res.get_node_values("Title")[0]]
                rows.append(row)
            with open(g.replace(" ", "_")+".csv", "w") as o:
                writer = csv.writer(o)
                writer.writerows(rows)
