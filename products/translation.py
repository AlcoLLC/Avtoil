from modeltranslation.translator import register, TranslationOptions
from .models import (Product_group, Segments,
    Oil_Types, Product, ProductProperty
)

@register(Product_group)
class ProductGroupTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'meta_title_prouduct_group', 'meta_description_prouduct_group')


@register(Segments)
class SegmentsTranslationOptions(TranslationOptions):
    fields = ('title', 'meta_title', 'meta_description')


@register(Oil_Types)
class OilTypesTranslationOptions(TranslationOptions):
    fields = ('title', 'meta_title', 'meta_description')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        'title', 'description', 'features_benefits', 'application',
        'recommendations', 'meta_title', 'meta_description', 'meta_keywords'
    )

@register(ProductProperty)
class ProductPropertyTranslationOptions(TranslationOptions):
    fields = ('property_name', 'unit', 'test_method', 'typical_value')
