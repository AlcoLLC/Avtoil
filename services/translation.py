from modeltranslation.translator import register, TranslationOptions
from .models import Service, ServiceContent, ServiceLastContent


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(ServiceContent)
class ServiceContentTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(ServiceLastContent)
class ServiceLastContentTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
