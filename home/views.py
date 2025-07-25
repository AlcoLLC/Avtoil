from django.shortcuts import render
from news.models import News
from services.models import Service, Service_Content
from products.models import Product_group
from .models import PartnerLogo, Gallery as GalleryImage, HomeSwiper

def home_view(request): 
    swiper_images = HomeSwiper.objects.filter(is_active=True).order_by('order')

    latest_news = News.objects.filter(is_active=True)[:3] 
    
    product_groups = Product_group.objects.all().order_by('-in_home', 'order')
    
    partner_logos = PartnerLogo.objects.all()

    images = GalleryImage.objects.all().order_by('order')

    service_contents = Service_Content.objects.filter(in_home=True)

    
    context = { 
        'swiper_images': swiper_images,
        'latest_news': latest_news, 
        'product_groups': product_groups,
        'partner_logos': partner_logos,
        'images': images,
        'service_contents': service_contents,
    } 
     
    return render(request, 'home.html', context)


def handler404(request, exception):
    """
    404 Error Handler
    """
    return render(request, '404.html', status=404)

def handler500(request):
    """
    500 Error Handler
    """
    return render(request, '500.html', status=500)

def handler403(request, exception):
    """
    403 Error Handler
    """
    return render(request, '403.html', status=403)

def handler400(request, exception):
    """
    400 Error Handler
    """
    return render(request, '400.html', status=400)
