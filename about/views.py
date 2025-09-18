from django.shortcuts import render
from .models import (
    AboutAvtoil, AboutContent, AboutLastContent, DocumentsCertification, Sustainability
)
from home.models import PartnerLogo, CarLogo, Gallery as GalleryImage

def about_page_view(request):
    about_avtoil = AboutAvtoil.objects.all()
    documents_cert = DocumentsCertification.objects.last()
    sustainability = Sustainability.objects.last()
    sustainability_image = sustainability.image if sustainability else None
    about_contents = AboutContent.objects.all()
    about_last_contents = AboutLastContent.objects.all()
    partner_logos = PartnerLogo.objects.all()
    car_logos = CarLogo.objects.all()
    images = GalleryImage.objects.all().order_by('order')

    context = {
        'about_avtoil': about_avtoil,
        'about_contents': about_contents,
        'about_last_contents': about_last_contents,
        'documents_cert': documents_cert,
        'sustainability': sustainability,
        'sustainability_image': sustainability_image,
        'partner_logos': partner_logos,
        'car_logos': car_logos,
        'images': images,
    }

    return render(request, 'about.html', context)