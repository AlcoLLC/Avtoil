from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from products.models import Product
from news.models import News
from brands.models import Brand_Portal_Content

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'
    
    def items(self):
        return [
            'home:home',
            'about:about',
            'products:product',
            'services:services', 
            'contact:contact',
            'partnership:partnership',
            'news:news',
            'faq:faq'
        ]
    
    def location(self, item):
        return reverse(item)

class HomeStaticSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['home:home'] 

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
        return reverse('news:news_detail', kwargs={'slug': obj.slug})

class FAQSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return []

    def location(self, obj):
        return reverse('faq:faq')  

class BrandPortalContentSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Brand_Portal_Content.objects.all().order_by('order')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('brands:brands') 

class AboutStaticSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return ['about:about']  

    def location(self, item):
        return reverse(item)

class ServicesStaticSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return ['services:services'] 

    def location(self, item):
        return reverse(item)

class PartnershipStaticSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return ['partnership:partnership']  
    def location(self, item):
        return reverse(item)

class ContactStaticSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return ['contact:contact'] 

    def location(self, item):
        return reverse(item)
    

sitemaps = {
    'home': HomeStaticSitemap,
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'news': NewsSitemap,
    'faq': FAQSitemap,
    'brands': BrandPortalContentSitemap,
    'about': AboutStaticSitemap,
    'services': ServicesStaticSitemap,
    'partnership': PartnershipStaticSitemap,
    'contact': ContactStaticSitemap,
}
