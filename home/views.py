from django.shortcuts import render
from news.models import News
from services.models import Service, Service_Content
from products.models import Product_group, Product
from about.models import Sustainability
from .models import PartnerLogo, Gallery as GalleryImage, HomeSwiper, BecomePartner, SolutionsHybrid, SolutionsHybridContent

def home_view(request): 
    swiper_images = HomeSwiper.objects.filter(is_active=True).order_by('order')
    latest_news = News.objects.filter(is_active=True)[:3]   
    product_groups = Product_group.objects.all().order_by('-in_home', 'order')  
    products = Product.objects.all().order_by('-in_home', 'order')  
    partner_logos = PartnerLogo.objects.all()
    images = GalleryImage.objects.all().order_by('order')
    service_contents = Service_Content.objects.filter(in_home=True)
    sustainability = Sustainability.objects.last()
    sustainability_image = sustainability.image if sustainability else None
    become_partner = BecomePartner.objects.last()      
    solutions_hybrid = SolutionsHybrid.objects.last()
    solutions_contents = solutions_hybrid.SolutionsHybrid.all()


    
    context = { 
        'swiper_images': swiper_images,
        'latest_news': latest_news, 
        'product_groups': product_groups,
        'products': products,
        'partner_logos': partner_logos,
        'images': images,
        'service_contents': service_contents,
        'sustainability_image': sustainability_image,
        'become_partner': become_partner,
        'solutions_hybrid': solutions_hybrid,
        'solutions_contents': solutions_contents,       
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
