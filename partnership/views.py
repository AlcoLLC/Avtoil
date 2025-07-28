from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Partnership, PartnerReview, PartnerFAQ, PartnershipForm, BusinessType
from home.models import PartnerLogo


def partnership_view(request):
    if request.method == 'POST':
        business_type_value = request.POST.get('typeOfBusiness')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        message = request.POST.get('message', '')
        
        if not all([business_type_value, first_name, last_name, email]):
            messages.error(request, _('Please fill in all required fields.'))
            return redirect('partnership:partnership')
        
        try:
            business_type = get_object_or_404(BusinessType, value=business_type_value, is_active=True)
            
            partnership_form = PartnershipForm(
                business_type=business_type,
                first_name=first_name.strip(),
                last_name=last_name.strip(),
                email=email.strip(),
                message=message.strip()
            )
            partnership_form.save()
            messages.success(request, _('Your partnership application has been submitted successfully. We will contact you soon.'))
            return redirect('partnership:partnership')
            
        except BusinessType.DoesNotExist:
            messages.error(request, _('Please select a valid business type.'))
            return redirect('partnership:partnership')
        except Exception as e:
            messages.error(request, _('An error occurred while submitting your application. Please try again.'))
            return redirect('partnership:partnership')

    partnerships = Partnership.objects.prefetch_related('Partnership').all()
    reviews = PartnerReview.objects.filter(is_active=True).order_by('-created_at')
    partner_faqs = PartnerFAQ.objects.filter(is_active=True).order_by('created_at')
    partner_logos = PartnerLogo.objects.all()
    
    # Active business types for dropdown
    business_types = BusinessType.objects.filter(is_active=True).order_by('order', 'name')

    context = {
        'partnerships': partnerships,
        'reviews': reviews,
        'partner_faqs': partner_faqs,
        'partner_logos': partner_logos,
        'business_types': business_types,
    }
    return render(request, 'partnership.html', context)