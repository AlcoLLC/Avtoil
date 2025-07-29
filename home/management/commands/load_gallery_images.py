import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from home.models import Gallery

class Command(BaseCommand):
    help = 'Load all .jpg images from ayarlaki folder into Gallery model'

    def handle(self, *args, **options):
        folder_path = 'AVTOIL_SITE_FOTO'
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')]

        for index, filename in enumerate(sorted(image_files)):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'rb') as f:
                gallery = Gallery()
                gallery.image.save(f"gallery/{filename}", File(f), save=True)
                gallery.order = index
                gallery.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(image_files)} images into Gallery'))
