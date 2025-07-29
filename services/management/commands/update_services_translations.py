from django.core.management.base import BaseCommand
from services.models import ( 
    Service,
    Service_Content,
)

class Command(BaseCommand):
    help = 'Copy original fields into *translate fields for Avtoil models'

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
            "Service": 0,
            "Service_Content": 0,
        }

        for item in Service.objects.all():
            if copy_fields(item, [
                ('title'),
                ('title_description'),
                ('description'),
            ]):
                updated_counts["Service"] += 1

        for item in Service_Content.objects.all():
            if copy_fields(item, [
                ('title'),
                ('description'),
            ]):
                updated_counts["Service_Content"] += 1


        self.stdout.write(self.style.SUCCESS("✅ Avtoil translations copied successfully."))
        for model, count in updated_counts.items():
            self.stdout.write(f"  - {model}: {count} updated")
