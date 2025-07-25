from modeltranslation.translator import register, TranslationOptions
from .models import HomeSwiper

@register(HomeSwiper)
class HomeSwiperTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'link')

