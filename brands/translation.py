from modeltranslation.translator import register, TranslationOptions
from .models import (
    Brand_Portal, Brand_Portal_Content
)

@register(Brand_Portal)
class BrandPortalTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Brand_Portal_Content)
class BrandPortalContentTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
