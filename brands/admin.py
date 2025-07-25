from django.contrib import admin
from .models import Brand_Portal, Brand_Portal_Content
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

class Brand_Portal_ContentInline(TranslationTabularInline):
    model = Brand_Portal_Content
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


@admin.register(Brand_Portal)
class Brand_PortalAdmin(TranslationAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)
    inlines = [Brand_Portal_ContentInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Brand_Portal_Content)
class Brand_Portal_ContentAdmin(TranslationAdmin):
    list_display = ('title', 'brand_portal', 'created_at', 'updated_at')
    list_filter = ('brand_portal', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
