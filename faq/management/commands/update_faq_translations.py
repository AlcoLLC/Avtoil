from django.core.management.base import BaseCommand
from faq.models import FAQ

class Command(BaseCommand):
    help = 'Copy default field values to translate fields for FAQ model'

    def handle(self, *args, **kwargs):
        updated_count = 0

        for faq in FAQ.objects.all():
            updated = False

            if updated:
                faq.save()
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated translation fields for {updated_count} FAQ(s).'
            )
        )
