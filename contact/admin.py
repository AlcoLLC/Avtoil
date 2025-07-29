from django.contrib import admin
from .models import Contact, ContactInfo
from modeltranslation.admin import TranslationAdmin


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company_name', 'email',
                   'phone_number', 'help_type', 'created_at')
    list_filter = ('help_type', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company_name', 'phone_number')
    readonly_fields = ('created_at', 'ip_address')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Company Information', {
            'fields': ('company_name',)
        }),
        ('Inquiry Details', {
            'fields': ('help_type', 'question')
        }),
        ('Additional Information', {
            'fields': ('created_at', 'ip_address')
        }),
    )

@admin.register(ContactInfo)
class ContactInfoAdmin(TranslationAdmin):
    list_display = ('title', 'contact_email', 'contact_phone')
    search_fields = ('title', 'description', 'contact_email')
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'description')
        }),
        ('Headquarters Information', {
            'fields': ('avtoil_headquarters', 'avtoil_headquarters_location', 'avtoil_headquarters_image')  
        }),
        ('Factory Information', {
            'fields': ('avtoil_factory', 'avtoil_factory_location', 'avtoil_factory_image') 
        }),
        ('Registration Information', {
            'fields': ('registers',)
        }),
        ('Contact Details', {
            'fields': ('contact_address',  'contact_phone', 'contact_email')
        }),
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

        