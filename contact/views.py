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
from smtplib import SMTPException
from django.core.mail import EmailMessage

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

def test_email_configuration():
    """Test email configuration and log results"""
    try:
        logger.info(f"Email Host: {settings.EMAIL_HOST}")
        logger.info(f"Email Port: {settings.EMAIL_PORT}")
        logger.info(f"Email User: {settings.EMAIL_HOST_USER}")
        logger.info(f"Use TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Not set')}")
        logger.info(f"Use SSL: {getattr(settings, 'EMAIL_USE_SSL', 'Not set')}")
        return True
    except Exception as e:
        logger.error(f"Email configuration error: {str(e)}")
        return False

def send_contact_emails(form_data, client_ip):
    """
    E-postaları göndermek için düzenlenmiş fonksiyon.
    Artık tek bir e-posta hem yöneticiye hem de kullanıcıya gönderiliyor.
    """
    try:
        # E-posta ayarlarını test et
        test_email_configuration()
        
        help_type_display = dict(Contact.HELP_CHOICES).get(form_data['help_type'])
        
        # Yönetici ve kullanıcı için ortak e-posta içeriği
        email_subject = f"İletişim Formu: {form_data['first_name']} {form_data['last_name']}"
        html_email = render_to_string('emails/contactform.html', {
            'first_name': form_data['first_name'],
            'last_name': form_data['last_name'],
            'company': form_data['company_name'],
            'email': form_data['email'],
            'phone_number': form_data['phone_number'],
            'help_type': help_type_display,
            'message': form_data['question'],
            'ip_address': client_ip,
        })
        
        # E-postayı hem yöneticiye hem de formu dolduran kullanıcıya gönder
        # Alıcı listesine kullanıcının e-postasını ekledik
        recipient_list = ['aytacmehdizade08@gmail.com', form_data['email']]
        
        email_message = EmailMessage(
            subject=email_subject,
            body=html_email,
            from_email=settings.EMAIL_HOST_USER,
            to=recipient_list,
        )
        email_message.content_subtype = "html"
        
        result = email_message.send(fail_silently=False)
        logger.info(f"E-posta gönderim sonucu: {result}. Alıcılar: {recipient_list}")
        
        return True, "E-posta başarıyla gönderildi."
        
    except SMTPException as smtp_error:
        error_msg = f"SMTP Hatası: {str(smtp_error)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg
    
    except Exception as e:
        error_msg = f"E-posta gönderme hatası: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg

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
        # reCAPTCHA verification
        recaptcha_response = request.POST.get('g-recaptcha-response')
        if not recaptcha_response or not verify_recaptcha(recaptcha_response):
            messages.error(request, _("reCAPTCHA verification failed. Please try again."))
            logger.warning("Form submission with invalid or missing reCAPTCHA.")
            return redirect('contact:contact')

        # IP address check - limit to 5 submissions per IP
        client_ip = get_client_ip(request)
        if client_ip:
            ip_submission_count = Contact.objects.filter(ip_address=client_ip).count()
            if ip_submission_count >= 5:
                messages.error(request, _("You have reached the maximum number of submissions (5) from this IP address."))
                logger.warning(f"IP address {client_ip} has reached submission limit: {ip_submission_count} submissions")
                return redirect('contact:contact')
            else:
                logger.info(f"IP address {client_ip} has {ip_submission_count} previous submissions, allowing new submission")

        # Form data preparation
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
                # Save contact instance
                contact_instance = form.save(commit=False)
                contact_instance.ip_address = client_ip 
                contact_instance.save()
                logger.info(f"Contact form saved successfully for {form_data['email']} from IP {client_ip}")
                
                # Send emails
                email_success, email_message = send_contact_emails(form.cleaned_data, client_ip)
                
                if email_success:
                    messages.success(request, _("Your message has been sent successfully. Thank you for contacting us!"))
                    logger.info(f"Contact form processed successfully for {form_data['email']}")
                    return redirect('/')
                else:
                    # Form was saved but emails failed
                    logger.error(f"Form saved but email failed: {email_message}")
                    messages.warning(request, _("Your message has been received, but there was an issue sending confirmation emails. We will contact you soon."))
                    return redirect('/')
                    
            except Exception as e:
                logger.error(f"Error processing form: {str(e)}", exc_info=True)
                messages.error(request, _("An error occurred while processing your message. Please try again or contact us directly."))
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