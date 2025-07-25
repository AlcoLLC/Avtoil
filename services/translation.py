from modeltranslation.translator import register, TranslationOptions
from .models import Service,  Service_Content, ServiceHighlight


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Service_Content)
class ServiceContentTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(ServiceHighlight)
class ServiceContentTranslationOptions(TranslationOptions):
    fields = ('title1', 'title2', 'title3')


