from .models import (
    AboutAminol, AboutSectionContent, Quality, QualityContent,
    WeGuarantee, Production, ProductionContent,
    DocumentsCertification, Sustainability, SustainabilityContent
)

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

class AboutSectionContentInline(TranslationTabularInline):
    model = AboutSectionContent
    extra = 1
    fields = ('title', 'description', 'image')

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(AboutAminol)
class AboutAminolAdmin(TranslationAdmin):
    inlines = [AboutSectionContentInline]
    fields = (
        'founded_year', 'based_in', 'location',
        'exporting_to', 'production_capacity', 'workforce', 'shared_image'
    )

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


# Quality Section Admin
class QualityContentInline(TranslationTabularInline):
    model = QualityContent
    extra = 1
    fields = ('title', 'description', 'image')

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Quality)
class QualityAdmin(admin.ModelAdmin):
    inlines = [QualityContentInline]


@admin.register(WeGuarantee)
class WeGuaranteeAdmin(TranslationAdmin):
    fields = (
        'title',
        'sub_title_one', 'sub_description_one',
        'sub_title_two', 'sub_description_two',
        'sub_title_three', 'sub_description_three',
        'sub_title_four', 'sub_description_four'
    )

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


# Production Section Admin
class ProductionContentInline(TranslationTabularInline):
    model = ProductionContent
    extra = 1
    fields = ('title', 'description', 'image')

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    inlines = [ProductionContentInline]


@admin.register(DocumentsCertification)
class DocumentsCertificationAdmin(TranslationAdmin):
    fields = ('title', 'description')

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


# Sustainability Section Admin
class SustainabilityContentInline(TranslationTabularInline):
    model = SustainabilityContent
    extra = 1

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Sustainability)
class SustainabilityAdmin(TranslationAdmin):
    inlines = [SustainabilityContentInline]
    fields = ('main_description',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
