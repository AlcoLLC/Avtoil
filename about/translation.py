from modeltranslation.translator import register, TranslationOptions
from .models import (
    AboutAvtoil, AboutContent, DocumentsCertification, Sustainability
)

from django.utils import translation
translation.activate('en')


@register(AboutAvtoil)
class AboutAvtoilTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(AboutContent)
class AboutContentTranslationOptions(TranslationOptions):
    fields = ('title', 'description')



@register(DocumentsCertification)
class DocumentsCertificationTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Sustainability)
class SustainabilityTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


