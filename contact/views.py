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

# Logger'ı yapılandıralım (projenizin logging ayarlarında daha detaylı yapabilirsiniz)
logger = logging.getLogger(__name__)

# --- Yardımcı Fonksiyonlar ---

def get_client_ip(request):
    """İstemcinin IP adresini güvenilir bir şekilde alır."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def verify_recaptcha(recaptcha_response, client_ip):
    """reCAPTCHA doğrulamasını yapar ve detaylı loglama sağlar."""
    if not recaptcha_response:
        logger.warning("reCAPTCHA yanıtı boş geldi.")
        return False
        
    data = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response,
        'remoteip': client_ip  # IP adresini de göndermek güvenliği artırır
    }
    try:
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data, timeout=10)
        response.raise_for_status()  # HTTP hatalarını yakalamak için
        result = response.json()
        logger.debug(f"reCAPTCHA doğrulama sonucu: {result}")
        
        if not result.get('success', False):
            error_codes = result.get('error-codes', [])
            logger.warning(f"reCAPTCHA doğrulaması BAŞARISIZ OLDU. Hata kodları: {error_codes}")
            return False
            
        logger.info(f"reCAPTCHA doğrulaması başarılı. IP: {client_ip}")
        return True
        
    except requests.RequestException as e:
        logger.error(f"reCAPTCHA servisine bağlanırken hata oluştu: {str(e)}")
        return False

def send_contact_emails(contact_instance):
    """Hem yöneticiye hem de kullanıcıya bildirim e-postalarını gönderir."""
    client_ip = contact_instance.ip_address
    
    # Seçimin ('buy', 'become_dealer' vb.) okunabilir metnini al
    help_type_display = dict(Contact.HELP_CHOICES).get(contact_instance.help_type)

    # 1. Yöneticiye gönderilecek e-posta
    try:
        admin_subject = f"Yeni İletişim Formu: {contact_instance.first_name} {contact_instance.last_name}"
        admin_html_content = render_to_string('emails/contactform.html', {
            'first_name': contact_instance.first_name,
            'last_name': contact_instance.last_name,
            'company': contact_instance.company_name,
            'email': contact_instance.email,
            'phone_number': contact_instance.phone_number,
            'help_type': help_type_display,
            'message': contact_instance.question,
            'ip_address': client_ip,
        })
        
        send_mail(
            admin_subject,
            '',  # Düz metin mesajı boş, çünkü HTML kullanıyoruz
            settings.EMAIL_HOST_USER,
            ['aytacmehdizade08@gmail.com'],  # Alıcı e-posta adresi
            html_message=admin_html_content,
            fail_silently=False, # Hata durumunda Exception fırlatır
        )
        logger.info(f"Yönetici e-postası başarıyla gönderildi: {contact_instance.email}")
    except Exception as e:
        logger.error(f"Yöneticiye e-posta gönderilirken HATA oluştu: {str(e)}", exc_info=True)
        # Bu hatayı yeniden fırlatarak, view'ın hatayı yakalamasını ve kullanıcıya bildirmesini sağlıyoruz
        raise e

    # 2. Kullanıcıya gönderilecek onay e-postası
    try:
        user_subject = "Avtoil İletişim Talebiniz Alındı"
        user_message = f"""
Sayın {contact_instance.first_name},

Avtoil ile iletişime geçtiğiniz için teşekkür ederiz. Talebinizi aldık. Ekibimiz en kısa sürede sizinle iletişime geçecektir.

Saygılarımızla,
Avtoil Destek Ekibi
"""
        send_mail(
            user_subject,
            user_message,
            settings.EMAIL_HOST_USER,
            [contact_instance.email], # Alıcı, formu dolduran kullanıcı
            fail_silently=False,
        )
        logger.info(f"Kullanıcıya onay e-postası başarıyla gönderildi: {contact_instance.email}")
    except Exception as e:
        # Kullanıcıya e-posta gitmemesi kritik bir hata değil, bu yüzden sadece loglayıp devam ediyoruz.
        logger.error(f"Kullanıcıya ({contact_instance.email}) onay e-postası gönderilirken HATA oluştu: {str(e)}", exc_info=True)


# --- Ana View Fonksiyonu ---

def contact_view(request):
    if request.method == 'POST':
        # reCAPTCHA doğrulaması
        recaptcha_response = request.POST.get('g-recaptcha-response')
        client_ip = get_client_ip(request)

        if not verify_recaptcha(recaptcha_response, client_ip):
            messages.error(request, _("reCAPTCHA doğrulaması başarısız oldu. Lütfen tekrar deneyin."))
            logger.warning(f"Geçersiz reCAPTCHA denemesi. IP: {client_ip}")
            return redirect('contact:contact')

        # DEĞİŞİKLİK 1: IP adresi gönderme limitini kontrol et
        if client_ip:
            submission_count = Contact.objects.filter(ip_address=client_ip).count()
            if submission_count >= 5:
                messages.error(request, _("Bu IP adresinden maksimum gönderme limitine ulaştınız. Lütfen daha sonra tekrar deneyin."))
                logger.warning(f"IP gönderme limitini aştı ({submission_count} deneme). IP: {client_ip}")
                return redirect('contact:contact')

        # Form verilerini işle
        form = ContactForm(request.POST)
        
        if form.is_valid():
            try:
                contact_instance = form.save(commit=False)
                contact_instance.ip_address = client_ip
                contact_instance.save()
                
                # DEĞİŞİKLİK 2: E-postaları ayrı bir fonksiyon ile gönder
                send_contact_emails(contact_instance)
                
                messages.success(request, _("Mesajınız başarıyla gönderildi. Bizimle iletişime geçtiğiniz için teşekkür ederiz!"))
                return redirect('/') # Ana sayfaya yönlendir
            
            except Exception as e:
                # E-posta gönderimi veya veritabanı kaydı sırasında oluşan hataları yakala
                logger.error(f"Form işlenirken veya e-posta gönderilirken genel bir hata oluştu: {str(e)}", exc_info=True)
                messages.error(request, _("Mesajınız gönderilirken bir hata oluştu. Lütfen daha sonra tekrar deneyin veya doğrudan bizimle iletişime geçin."))
                return redirect('contact:contact')
        else:
            # Form geçerli değilse hataları kullanıcıya göster
            logger.warning(f"Form doğrulama hataları: {form.errors.as_json()}")
            for field, errors in form.errors.items():
                for error in errors:
                    # Alan adını daha okunabilir yap
                    field_name = field.replace('_', ' ').title()
                    messages.error(request, f"{field_name}: {error}")
            return redirect('contact:contact')

    # GET isteği için
    contact_info = ContactInfo.objects.last()
    context = {
        'contact_info': contact_info,
        'form': ContactForm(), # Boş form
        'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
    }
    
    return render(request, 'contact.html', context)