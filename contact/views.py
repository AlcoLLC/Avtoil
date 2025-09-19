# contact/views.py

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

# Hataları ve işlemleri takip etmek için logger kurulumu
logger = logging.getLogger(__name__)

def get_client_ip(request):
    """Kullanıcının IP adresini alır"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def verify_recaptcha(recaptcha_response, client_ip=None):
    """Google reCAPTCHA doğrulamasını yapar"""
    if not settings.RECAPTCHA_SECRET_KEY:
        logger.error("RECAPTCHA_SECRET_KEY ayarlanmamış.")
        return False

    data = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    if client_ip:
        data['remoteip'] = client_ip

    try:
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data, timeout=5)
        response.raise_for_status()
        result = response.json()
        logger.debug(f"reCAPTCHA doğrulama sonucu: {result}")
        if not result.get('success', False):
            logger.warning(f"reCAPTCHA doğrulaması başarısız oldu: {result.get('error-codes')}")
            return False
        return True
    except requests.RequestException as e:
        logger.error(f"reCAPTCHA doğrulama isteği başarısız: {str(e)}")
        return False

def contact_view(request):
    contact_info = ContactInfo.objects.last()
    
    if request.method == 'POST':
        client_ip = get_client_ip(request)
        
        # 1. reCAPTCHA Doğrulaması
        recaptcha_response = request.POST.get('g-recaptcha-response')
        if not recaptcha_response or not verify_recaptcha(recaptcha_response, client_ip):
            messages.error(request, _("reCAPTCHA verification failed. Please try again."))
            logger.warning(f"Geçersiz reCAPTCHA denemesi. IP: {client_ip}")
            # Hata durumunda formu ve girilen verileri korumak için sayfayı yeniden render et
            return render(request, 'contact.html', {'contact_info': contact_info})

        # 2. IP Adresi Gönderim Limiti Kontrolü (5'e çıkarıldı)
        if client_ip:
            submission_count = Contact.objects.filter(ip_address=client_ip).count()
            if submission_count >= 5:
                messages.error(request, _("You have reached the maximum number of submissions from this IP address."))
                logger.warning(f"Gönderim limitini aşan IP: {client_ip}")
                return render(request, 'contact.html', {'contact_info': contact_info})

        # 3. Form Verisi Eşleştirmesi (KRİTİK DÜZELTME)
        # HTML'den gelen 'firstName' gibi isimleri formun beklediği 'first_name' gibi isimlere eşleştiriyoruz.
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
                logger.info(f"Yeni iletişim formu kaydedildi. IP: {client_ip}")

                # E-posta için yardım türünün okunabilir metnini al
                help_type_display = form.instance.get_help_type_display()
                
                # Yönetici Bildirim E-postası
                admin_subject = f"Yeni İletişim Formu: {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}"
                admin_html_content = render_to_string('emails/contactform.html', {
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
                    admin_subject, '', settings.EMAIL_HOST_USER,
                    ['aytacmehdizade08@gmail.com'], # Yönetici e-posta adresi
                    html_message=admin_html_content,
                    fail_silently=False
                )

                # Kullanıcı Onay E-postası
                user_subject = _("Thank you for contacting Avtoil")
                user_html_content = f"Dear {form.cleaned_data['first_name']},<br><br>Thank you for contacting Avtoil. We have received your inquiry. Our team will get back to you shortly.<br><br>Best regards,<br>Avtoil Support Team"
                
                send_mail(
                    user_subject, '', settings.EMAIL_HOST_USER,
                    [form.cleaned_data['email']],
                    html_message=user_html_content,
                    fail_silently=False
                )
                
                messages.success(request, _("Your message has been sent successfully. Thank you for contacting us!"))
                return redirect('/') # Başarılı olunca ana sayfaya yönlendir
            
            except Exception as e:
                logger.error(f"Form işlenirken veya e-posta gönderilirken hata oluştu: {str(e)}", exc_info=True)
                messages.error(request, _("An error occurred while sending your message. Please try again or contact us directly."))
        
        else: # Form geçersizse
            logger.warning(f"Form doğrulama hataları: {form.errors.as_json()}")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    
    # GET isteği veya başarısız POST sonrası için context
    context = {
        'contact_info': contact_info,
        'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
    }
    
    return render(request, 'contact.html', context)