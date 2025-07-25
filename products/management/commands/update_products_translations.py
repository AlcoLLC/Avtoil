from django.core.management.base import BaseCommand
from products.models import (
    Product_group, Segments, Oil_Types, Product
)

class Command(BaseCommand):
    help = 'Copy original values to *translate fields in Product-related models'

    def handle(self, *args, **options):
        def copy_fields(instance, field_pairs):
            updated = False
            for original, translated in field_pairs:
                if not getattr(instance, translated, None):
                    setattr(instance, translated, getattr(instance, original, ''))
                    updated = True
            if updated:
                instance.save()
            return updated

        updated_counts = {
            "Product_group": 0,
            "Segments": 0,
            "Oil_Types": 0,
            "Product": 0,
        }

        for pg in Product_group.objects.all():
            if copy_fields(pg, [
                ('title'),
                ('description'),
            ]):
                updated_counts["Product_group"] += 1

        for seg in Segments.objects.all():
            if copy_fields(seg, [('title')]):
                updated_counts["Segments"] += 1

        for ot in Oil_Types.objects.all():
            if copy_fields(ot, [('title')]):
                updated_counts["Oil_Types"] += 1

        for prod in Product.objects.all():
            if copy_fields(prod, [
                ('title'),
                ('description'),
                ('features_benefits'),
                ('application'),
                ('recommendations'),
            ]):
                updated_counts["Product"] += 1

        self.stdout.write(self.style.SUCCESS("✅ Translations copied successfully."))
        for model, count in updated_counts.items():
            self.stdout.write(f"  - {model}: {count} updated")
