from django.shortcuts import render
from .models import Partnership, PartnerReview, PartnerFAQ
from home.models import PartnerLogo


def partnership_view(request):

    partnerships = Partnership.objects.prefetch_related('Partnership').all()
    reviews = PartnerReview.objects.filter(is_active=True).order_by('-created_at')
    partner_faqs = PartnerFAQ.objects.filter(is_active=True).order_by('created_at')
    partner_logos = PartnerLogo.objects.all()

    context = {
        'partnerships': partnerships,
        'reviews': reviews,
        'partner_faqs': partner_faqs,
        'partner_logos':partner_logos,
    }
    return render(request, 'partnership.html', context)