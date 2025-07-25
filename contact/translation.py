from modeltranslation.translator import register, TranslationOptions
from .models import ContactInfo

@register(ContactInfo)
class ContactInfoTranslationOptions(TranslationOptions):
    fields = (
        'title', 'description', 
        'aminol_headquarters', 'aminol_factory',
        'registers', 'contact_address'
    )
