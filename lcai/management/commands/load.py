import os
import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from arches.app.models.models import MapLayer

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('operation',
                            choices=['full', 'check-resources'],
                            help='Operation Type; ' +
                                 '\'full\'=Loads reference data and resource graphs.')

    def handle(self, *args, **options):
        if options['operation'] == 'full':
            call_command('packages',operation="setup_db")
            self.load_reference_data()
            call_command('packages',operation="import_graphs")
            self.switch_basemap_layer()
            call_command('packages',operation="import_business_data",
                            overwrite="overwrite",bulk_load=True)

        elif options['operation'] == 'check-resources':
            self.check_resources()

    def load_reference_data(self):
        thesauri = os.path.join(settings.APP_ROOT,"db","schemes","thesauri")
        for f in os.listdir(thesauri):
            if f.endswith(".rdf"):
                call_command("packages",operation="import_reference_data",
                    source=os.path.join(thesauri,f))
        
        collections = os.path.join(settings.APP_ROOT,"db","schemes","collections")
        for f in os.listdir(collections):
            if f.endswith(".rdf"):
                call_command("packages",operation="import_reference_data",
                    source=os.path.join(collections,f))
    
    def switch_basemap_layer(slef):
        
        streets = MapLayer.objects.get(name="streets")
        streets.addtomap = False
        streets.save()
        
        satellite = MapLayer.objects.get(name="satellite")
        satellite.addtomap = True
        satellite.save()


    def check_resources(self):

        media_dir = Path(settings.MEDIA_ROOT, "uploadedfiles")
        package_path = Path("../lcai-pkg")
        bd = Path(package_path, "business_data")

        files_to_check = {
            "all-images.csv": {
                "file_fields": [
                    "filename",
                    "thumbnail"
                ]
            },
            "all-3d-panels_v6.csv": {
                "file_fields": [
                    "Thumbnail Image",
                ]
            },
        }

        missing = []
        used = []
        for f, v in files_to_check.items():
            print(f"---{f}---")

            path = Path(bd, f)

            with open(path, "r") as o:
                reader = csv.reader(o)

                headers = next(reader)                
                for row in reader:
                    for field in v['file_fields']:
                        fn = row[headers.index(field)]
                        p1 = Path(media_dir, fn)

                        if p1.is_file():
                            used.append(p1)
                        else:
                            missing.append(p1)
                            print(p1)

        jpgs = [i for i in media_dir.glob("*.jpg")]
        unused = [i for i in jpgs if not i in used]
        print(f"{len(jpgs)} total images")
        print(f"{len(used)} used images")
        print(f"{len(missing)} missing images")
        # for i in sorted(missing):
        #     print(i.name)
        print(f"{len(unused)} unused images")