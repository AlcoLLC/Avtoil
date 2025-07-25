from django.core.management.base import BaseCommand
from brands.models import Brand_Portal, Brand_Portal_Content 

class Command(BaseCommand):
    help = 'Copy default field values to translate fields for multilingual models'

    def handle(self, *args, **options):

        def update_instance_fields(instance, field_pairs):
            for original_field, translate_field in field_pairs:
                original_value = getattr(instance, original_field, '')
                if not getattr(instance, translate_field, None):
                    setattr(instance, translate_field, original_value)

        model_configs = [
            (Brand_Portal, [('title'), ('description')]),
            (Brand_Portal_Content, [('title'), ('description)]),
        ]

        for model, field_pairs in model_configs:
            for instance in model.objects.all():
                update_instance_fields(instance, field_pairs)
                instance.save()

        self.stdout.write(self.style.SUCCESS("Successfully copied values to translate fields."))