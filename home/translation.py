from modeltranslation.translator import register, TranslationOptions
from .models import HomeSwiper, SolutionsHybrid, SolutionsHybridContent, BecomePartner, Review

@register(HomeSwiper)
class HomeSwiperTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'link')

@register(BecomePartner)
class BecomePartnerTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(SolutionsHybrid)
class SolutionsHybridTranslationOptions(TranslationOptions):
    fields = ('title', 'description_left', 'description_right')

@register(SolutionsHybridContent)
class SolutionsHybridContentTranslationOptions(TranslationOptions):
    fields = ('content',)

@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('summary', 'review')
