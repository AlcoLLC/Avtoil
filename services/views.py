from django.shortcuts import render
from .models import (
    Service,
    Service_Content,
    ServiceHighlight
)
from home.models import PartnerLogo, Gallery as  Supplier
from django.utils.translation import gettext_lazy as _


def service_view(request):
    services = Service.objects.all()
    service_contents = Service_Content.objects.all() 
    partner_logos = PartnerLogo.objects.all()
    service_highlights = ServiceHighlight.objects.first()
    context = {
        'services': services,
        'service_contents': service_contents,
        'partner_logos': partner_logos,
        'service_highlights': service_highlights,
    }
    
    return render(request, 'service.html', context)
