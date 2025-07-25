from modeltranslation.translator import register, TranslationOptions
from .models import (
    AboutAminol, AboutSectionContent, QualityContent, WeGuarantee,
    ProductionContent, DocumentsCertification, Sustainability, SustainabilityContent
)

from django.utils import translation
translation.activate('en')


@register(AboutAminol)
class AboutAminolTranslationOptions(TranslationOptions):
    fields = ('based_in', 'location', 'exporting_to', 'production_capacity')


@register(AboutSectionContent)
class AboutSectionContentTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(QualityContent)
class QualityContentTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(WeGuarantee)
class WeGuaranteeTranslationOptions(TranslationOptions):
    fields = (
        'title', 'sub_title_one', 'sub_description_one',
        'sub_title_two', 'sub_description_two',
        'sub_title_three', 'sub_description_three',
        'sub_title_four', 'sub_description_four'
    )


@register(ProductionContent)
class ProductionContentTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(DocumentsCertification)
class DocumentsCertificationTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Sustainability)
class SustainabilityTranslationOptions(TranslationOptions):
    fields = ('main_description',)


@register(SustainabilityContent)
class SustainabilityContentTranslationOptions(TranslationOptions):
    fields = ('title', 'description')