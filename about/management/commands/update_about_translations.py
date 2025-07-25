from django.core.management.base import BaseCommand
from about.models import (
    AboutAminol, AboutSectionContent, QualityContent, WeGuarantee,
    ProductionContent, DocumentsCertification, Sustainability, SustainabilityContent
)


class Command(BaseCommand):
    help = 'Copy original field values to corresponding translate fields'

    def handle(self, *args, **options):
        
        # AboutAminol model
        self.stdout.write('Processing AboutAminol...')
        for instance in AboutAminol.objects.all():
            instance.based_in = instance.based_in
            instance.location = instance.location
            instance.exporting_to = instance.exporting_to
            instance.production_capacity = instance.production_capacity
            instance.save()
        
        # AboutSectionContent model
        self.stdout.write('Processing AboutSectionContent...')
        for instance in AboutSectionContent.objects.all():
            instance.title = instance.title
            instance.description = instance.description
            instance.save()
        
        # QualityContent model
        self.stdout.write('Processing QualityContent...')
        for instance in QualityContent.objects.all():
            instance.title = instance.title
            instance.description = instance.description
            instance.save()
        
        # WeGuarantee model
        self.stdout.write('Processing WeGuarantee...')
        for instance in WeGuarantee.objects.all():
            instance.title = instance.title
            instance.sub_title_one = instance.sub_title_one
            instance.sub_description_one = instance.sub_description_one
            instance.sub_title_two = instance.sub_title_two
            instance.sub_description_two = instance.sub_description_two
            instance.sub_title_three = instance.sub_title_three
            instance.sub_description_three = instance.sub_description_three
            instance.sub_title_four = instance.sub_title_four
            instance.sub_description_four = instance.sub_description_four
            instance.save()
        
        # ProductionContent model
        self.stdout.write('Processing ProductionContent...')
        for instance in ProductionContent.objects.all():
            instance.title = instance.title
            instance.description = instance.description
            instance.save()
        
        # DocumentsCertification model
        self.stdout.write('Processing DocumentsCertification...')
        for instance in DocumentsCertification.objects.all():
            instance.title = instance.title
            instance.description = instance.description
            instance.save()
        
        # Sustainability model
        self.stdout.write('Processing Sustainability...')
        for instance in Sustainability.objects.all():
            instance.main_description = instance.main_description
            instance.save()
        
        # SustainabilityContent model
        self.stdout.write('Processing SustainabilityContent...')
        for instance in SustainabilityContent.objects.all():
            instance.title = instance.title
            instance.description = instance.description
            instance.save()

            self.stdout.write(
            self.style.SUCCESS(
                'Successfully copied all original field values to  fields!'
            )
        )