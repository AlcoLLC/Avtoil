from modeltranslation.translator import register, TranslationOptions
from .models import ContactInfo

@register(ContactInfo)
class ContactInfoTranslationOptions(TranslationOptions):
    fields = (
        'title', 'description', 
        'avtoil_headquarters', 'avtoil_factory', 
        'registers', 'contact_address'
    )