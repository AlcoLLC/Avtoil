from django.contrib import admin
from django.utils.html import format_html
from .models import Partnership, Partnership_Content, PartnerReview, PartnerFAQ, PartnershipForm, BusinessType
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

class PartnershipContentInline(TranslationTabularInline):
    model = Partnership_Content
    extra = 1

@admin.register(Partnership)
class PartnershipAdmin(TranslationAdmin):
    list_display = ('title', 'main_image_preview', 'secondary_image_preview')
    search_fields = ('title', 'description')
    
    fields = ('title',  'description',  'main_image', 'secondary_image')
    inlines = [PartnershipContentInline]
    
    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="width: 60px; height: 40px; object-fit: cover;" />', obj.main_image.url)
        return "Yoxdur"
    main_image_preview.short_description = "Main"

    def secondary_image_preview(self, obj):
        if obj.secondary_image:
            return format_html('<img src="{}" style="width: 60px; height: 40px; object-fit: cover;" />', obj.secondary_image.url)
        return "Yoxdur"
    secondary_image_preview.short_description = "Secondary"


@admin.register(Partnership_Content)
class PartnershipContentAdmin(TranslationAdmin):
    list_display = ('title', 'Partnership')
    list_filter = ('Partnership',)
    search_fields = ('title',)
    
    fields = ('Partnership', 'title')


@admin.register(PartnerReview)
class PartnerReviewAdmin(TranslationAdmin):
    list_display = ('name', 'created_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'review')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'image', 'is_active', 'position')
        }),
        ('Contents', {
            'fields': ('review',)
        }),
    )


@admin.register(PartnerFAQ)
class PartnerFAQAdmin(TranslationAdmin):
    list_display = ('question', 'order', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_active')
    fieldsets = (
        (None, {
            'fields': ('question', 'answer')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
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


@admin.register(BusinessType)
class BusinessTypeAdmin(TranslationAdmin):
    list_display = ('name', 'value', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'value')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'name')
    
    fields = ('name', 'value', 'is_active', 'order')


@admin.register(PartnershipForm)
class PartnershipFormAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'business_type', 'created_at', 'is_processed')
    list_filter = ('business_type', 'is_processed', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'business_type__name')
    readonly_fields = ('created_at',)
    list_editable = ('is_processed',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Business Information', {
            'fields': ('business_type', 'message')
        }),
        ('Status', {
            'fields': ('is_processed', 'created_at')
        }),
    )

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'