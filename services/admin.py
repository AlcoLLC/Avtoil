from django.contrib import admin
from django.contrib import messages
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import (
    Service,
    Service_Content,
    ServiceHighlight
)

class Service_ContentInline(TranslationTabularInline):
    model = Service_Content
    extra = 1


@admin.register(Service)
class ServiceAdmin(TranslationAdmin):
    list_display = ('title',)
    search_fields = ('title',)

    fields = (
        'title', 'description', 'image'
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


@admin.register(Service_Content)
class ServiceContentAdmin(TranslationAdmin):
    list_display = ('title', 'in_home',)
    search_fields = ('title', )
    
    fields = (
        'title', 
        'description', 
        'image', 
        'in_home'
    )


@admin.register(ServiceHighlight)
class ServiceHighlightAdmin(TranslationAdmin):
    fields = ('title1', 'image1', 'title2', 'image2', 'title3', 'image3')
    list_display = ('title1', 'title2', 'title3')

    def has_add_permission(self, request):
        if ServiceHighlight.objects.exists():
            return False
        return True

    def changelist_view(self, request, extra_context=None):
        if not ServiceHighlight.objects.exists():
            messages.info(request, "Please add the data only once. ")
        return super().changelist_view(request, extra_context)
