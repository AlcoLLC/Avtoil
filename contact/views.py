from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from .models import Contact, ContactInfo
from .forms import ContactForm
import logging
import requests
from django.utils.translation import gettext_lazy as _

RECAPTCHA_SITE_KEY = settings.RECAPTCHA_SITE_KEY
RECAPTCHA_SECRET_KEY = settings.RECAPTCHA_SECRET_KEY
logger = logging.getLogger(__name__)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def verify_recaptcha(recaptcha_response):
    data = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    try:
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data, timeout=5)
        response.raise_for_status()
        result = response.json()
        logger.debug(f"reCAPTCHA verification result: {result}")
        return result.get('success', False)
    except requests.RequestException as e:
        logger.error(f"reCAPTCHA verification error: {str(e)}")
        return False

def contact_view(request):
    help_choices = [
        ('buy', _('I would like to buy Avtoil products.')),
        ('become_dealer', _('I am interested in becoming a distributor.')),
        ('technical', _('I need technical support.')),
        ('other', _('Other'))
    ]

    form_labels = {
        'help_type': _('How can we help you?'),
        'company': _('Company name'),
        'question': _('Your question, wish and/or clarification'),
        'first_name': _('First name'),
        'last_name': _('Last name'),
        'email': _('Email address'),
        'phone': _('Phone number'),
        'required': '*',
        'send_button': _('Send')
    }
    
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        if not recaptcha_response or not verify_recaptcha(recaptcha_response):
            messages.error(request, _("reCAPTCHA verification failed. Please try again."))
            logger.warning("Form submission with invalid or missing reCAPTCHA.")
            return redirect('contact:contact')

        client_ip = get_client_ip(request)
        if client_ip and Contact.objects.filter(ip_address=client_ip).exists():
            messages.error(request, _("You have already submitted the form from this IP address."))
            logger.warning(f"Duplicate submission attempt from IP address {client_ip}.")
            return redirect('contact:contact')

        form_data = {
            'help_type': request.POST.get('helpType'),
            'company_name': request.POST.get('company'),
            'question': request.POST.get('question'),
            'first_name': request.POST.get('firstName'),
            'last_name': request.POST.get('lastName'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone'),
        }
        
        form = ContactForm(form_data)
        
        if form.is_valid():
            try:
                contact_instance = form.save(commit=False)
                contact_instance.ip_address = client_ip 
                contact_instance.save()
                
                help_type_display = dict(Contact.HELP_CHOICES).get(form.cleaned_data['help_type'])
                
                email_subject = f"New Contact Form Submission from {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}"
                html_email = render_to_string('emails/contactform.html', {
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'company': form.cleaned_data['company_name'],
                    'email': form.cleaned_data['email'],
                    'phone_number': form.cleaned_data['phone_number'],
                    'help_type': help_type_display,
                    'message': form.cleaned_data['question'],
                    'ip_address': client_ip,
                })
                
                send_mail(
                    email_subject,
                    '',
                    settings.EMAIL_HOST_USER,
                    ['info@aminol.az'],
                    html_message=html_email,
                    fail_silently=False,
                )
                
                user_email_subject = "Thank you for contacting Aminol"
                user_email_message = f"""
Dear {form.cleaned_data['first_name']},

Thank you for contacting Aminol. We have received your inquiry. Our team will get back to you shortly.

Best regards,
Aminol Support Team
"""
                send_mail(
                    user_email_subject,
                    user_email_message,
                    settings.EMAIL_HOST_USER,
                    [form.cleaned_data['email']],
                    fail_silently=False,
                )
                
                messages.success(request, _("Your message has been sent successfully. Thank you for contacting us!"))
                return redirect('/')
            
            except Exception as e:
                logger.error(f"Error processing form or sending email: {str(e)}", exc_info=True)
                messages.error(request, _("An error occurred while sending your message. Please try again or contact us directly."))
                return redirect('contact:contact')
        else:
            logger.warning(f"Form validation errors: {form.errors.as_json()}")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
            return redirect('contact:contact')

    contact_info = ContactInfo.objects.last()
    context = {
        'help_choices': help_choices,
        'contact_info': contact_info,
        'form_labels': form_labels,
        'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY, 
    }
    
    return render(request, 'contact.html', context)