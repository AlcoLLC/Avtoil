from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from products.models import Product, Product_group, Segments, Oil_Types, Viscosity
from news.models import News
from faq.models import FAQ
from about.models import AboutAvtoil, AboutContent, Sustainability, DocumentsCertification
from brands.models import Brand_Portal, Brand_Portal_Content
from services.models import Service
class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'
    
    def items(self):
        return [
            'home:home',
            'about:about_page',
            'products:product_list',
            'services: services_page', 
            'contact:contact',
            'partnership:partnership',
            'news:news_list',
            'faq:faq'
        ]
    
    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Product.objects.all()
    
    def lastmod(self, obj):
        return obj.created_at
    
    def location(self, obj):
        return reverse('products:product_detail', kwargs={'slug': obj.slug})


class NewsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7
    
    def items(self):
        return News.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.published_date
    
    def location(self, obj):
        return reverse('news:news_detail', kwargs={'pk': obj.pk})


class FAQSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return FAQ.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        # FAQ için spesifik URL pattern bulunamadı, 
        # muhtemelen faq:faq_detail olmalı
        return reverse('faq:faq_detail', kwargs={'id': obj.id})


class BrandPortalContentSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5
    
    def items(self):
        return Brand_Portal_Content.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        # Brand portal content için spesifik detail URL'i brands.urls'de görünmüyor
        # Bu sınıfı kaldırabilir ya da uygun URL pattern ekleyebilirsiniz
        return reverse('brands:brand_portal_content_detail', kwargs={'id': obj.id})



class AboutSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    
    def items(self):
        about_pages = []
        
        # about.urls'de sadece 'about_page' var
        # Diğer sayfalar için URL pattern'ler eklenmeli
        if AboutAvtoil.objects.exists():
            about_pages.append('about:about_aminol')
            
        if Quality.objects.exists():
            about_pages.append('about:quality')
            
        if Production.objects.exists():
            about_pages.append('about:production')
            
        if Sustainability.objects.exists():
            about_pages.append('about:sustainability')
            
        if WeGuarantee.objects.exists():
            about_pages.append('about:we_guarantee')
            
        if DocumentsCertification.objects.exists():
            about_pages.append('about:documents_certification')
            
        return about_pages
    
    def location(self, item):
        return reverse(item)


class WeGuaranteeSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return WeGuarantee.objects.all()
    
    def location(self, obj):
        return reverse('about:we_guarantee_detail', kwargs={'id': obj.id})


class DocumentsCertificationSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return DocumentsCertification.objects.all()
    
    def location(self, obj):
        return reverse('about:documents_certification_detail', kwargs={'id': obj.id})


class ServicesSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    
    def items(self):
        services = []
        services.extend([
            'services:services_page',
        ])
            
        return services
    
    def location(self, item):
        return reverse(item)




# Mevcut URL pattern'lere göre çalışacak sitemaps
sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'news': NewsSitemap,
    # Aşağıdaki sitemaps için önce URL pattern'ler eklenmeli:
    # 'faq': FAQSitemap,
    # 'brand_portal_content': BrandPortalContentSitemap,
    # 'about': AboutSitemap,
    # 'we_guarantee': WeGuaranteeSitemap,
    # 'documents_certification': DocumentsCertificationSitemap,
    # 'services': ServicesSitemap,
}