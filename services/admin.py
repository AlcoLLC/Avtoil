from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import Service, ServiceContent, ServiceLastContent

class ServiceContentInline(TranslationTabularInline):
    model = ServiceContent
    extra = 1
    fields = ('title', 'description', 'image', 'in_home')


@admin.register(Service)
class ServiceAdmin(TranslationAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    inlines = [ServiceContentInline]
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(ServiceContent)
class ServiceContentAdmin(TranslationAdmin):
    list_display = ('title', 'service', 'in_home')
    list_filter = ('in_home', 'service') 
    search_fields = ('title', 'description')
    fields = ('service', 'title', 'description', 'image', 'in_home')


@admin.register(ServiceLastContent)
class ServiceLastContentAdmin(TranslationAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    fields = ('title', 'description', 'image')
