# views.py

from django.shortcuts import render
from .models import Service, ServiceLastContent
from home.models import PartnerLogo
from django.utils.translation import gettext_lazy as _


def service_view(request):
    services = Service.objects.prefetch_related('service').all()
    service_last_content = ServiceLastContent.objects.first()
    partner_logos = PartnerLogo.objects.all()
    
    context = {
        'services': services,
        'service_last_content': service_last_content, 
        'partner_logos': partner_logos,
    }
    
    return render(request, 'service.html', context)