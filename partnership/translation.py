from modeltranslation.translator import register, TranslationOptions
from .models import Partnership, Partnership_Content, PartnerReview, PartnerFAQ

@register(Partnership)
class PartnershipTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Partnership_Content)
class PartnershipContentTranslationOptions(TranslationOptions):
    fields = ('title', )


@register(PartnerReview)
class PartnerReviewTranslationOptions(TranslationOptions):
    fields = ('name', 'position', 'review')

@register(PartnerFAQ)
class PartnerFAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')