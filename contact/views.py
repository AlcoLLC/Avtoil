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
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def verify_recaptcha(recaptcha_response, client_ip=None):
    """Verify reCAPTCHA response with better error handling"""
    
    if not recaptcha_response:
        logger.warning("Empty reCAPTCHA response received")
        return False
    
    if not RECAPTCHA_SECRET_KEY:
        logger.error("RECAPTCHA_SECRET_KEY not configured")
        return False
    
    # Clean the response
    recaptcha_response = recaptcha_response.strip()
    
    data = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    
    # Add IP address if available
    if client_ip:
        data['remoteip'] = client_ip
    
    try:
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', 
            data=data, 
            timeout=15
        )
        
        logger.debug(f"reCAPTCHA verification HTTP status: {response.status_code}")
        response.raise_for_status()
        
        result = response.json()
        logger.debug(f"reCAPTCHA verification result: {result}")
        
        if not result.get('success', False):
            error_codes = result.get('error-codes', [])
            logger.warning(f"reCAPTCHA verification failed with error codes: {error_codes}")
            return False
        
        logger.info("reCAPTCHA verification successful")
        return True
        
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
        # Get reCAPTCHA response
        recaptcha_response = request.POST.get('g-recaptcha-response')
        client_ip = get_client_ip(request)
        
        # Verify reCAPTCHA
        if not recaptcha_response or not verify_recaptcha(recaptcha_response, client_ip):
            messages.error(request, _("reCAPTCHA verification failed. Please try again."))
            logger.warning("Form submission with invalid or missing reCAPTCHA.")
            return redirect('contact:contact')

        # Check IP submission limit (allow 5 submissions per IP)
        if client_ip:
            existing_submissions = Contact.objects.filter(ip_address=client_ip).count()
            logger.info(f"Existing submissions from IP {client_ip}: {existing_submissions}")
            
            if existing_submissions >= 5:
                messages.error(request, _("Maximum number of submissions (5) reached from this IP address. Please contact us directly."))
                logger.warning(f"IP address {client_ip} exceeded submission limit (5).")
                return redirect('contact:contact')

        # Prepare form data
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
                # Save the contact form
                contact_instance = form.save(commit=False)
                contact_instance.ip_address = client_ip 
                contact_instance.save()
                
                logger.info(f"Contact form saved successfully with ID: {contact_instance.id}")
                
                # Send emails
                send_contact_emails(contact_instance, form.cleaned_data)
                
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

def send_contact_emails(contact_instance, cleaned_data):
    """Send both admin notification and user confirmation emails"""
    
    logger.info(f"Starting email send process for contact: {cleaned_data['email']}")
    
    try:
        # Get help type display name
        help_type_display = dict(Contact.HELP_CHOICES).get(cleaned_data['help_type'])
        
        # 1. Admin notification email
        admin_subject = f"New Contact Form Submission from {cleaned_data['first_name']} {cleaned_data['last_name']}"
        admin_html_email = render_to_string('emails/contactform.html', {
            'first_name': cleaned_data['first_name'],
            'last_name': cleaned_data['last_name'],
            'company': cleaned_data['company_name'],
            'email': cleaned_data['email'],
            'phone_number': cleaned_data['phone_number'],
            'help_type': help_type_display,
            'message': cleaned_data['question'],
            'ip_address': contact_instance.ip_address,
        })
        
        # Get admin email from settings or use default
        admin_emails = getattr(settings, 'CONTACT_ADMIN_EMAIL', ['info@avtoil.de'])
        if isinstance(admin_emails, str):
            admin_emails = [admin_emails]
        
        send_mail(
            subject=admin_subject,
            message='',  # Plain text fallback
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=admin_emails,
            html_message=admin_html_email,
            fail_silently=False,
        )
        
        logger.info(f"Admin notification email sent successfully to {admin_emails}")
        
        # 2. User confirmation email
        user_subject = _("Thank you for contacting Avtoil")
        user_message = f"""
Dear {cleaned_data['first_name']},

Thank you for contacting Avtoil. We have received your inquiry and our team will get back to you shortly.

Your submission details:
- Help Type: {help_type_display}
- Company: {cleaned_data.get('company_name', 'N/A')}
- Message: {cleaned_data['question'][:100]}{'...' if len(cleaned_data['question']) > 100 else ''}

Best regards,
Avtoil Support Team
"""
        
        send_mail(
            subject=user_subject,
            message=user_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[cleaned_data['email']],
            fail_silently=False,
        )
        
        logger.info(f"User confirmation email sent successfully to {cleaned_data['email']}")
        
    except Exception as e:
        logger.error(f"Failed to send emails: {str(e)}", exc_info=True)
        raise  # Re-raise to trigger error message in view