from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Contact(models.Model):
    HELP_CHOICES = [
        ('buy', _('I would like to buy Aminol products.')),
        ('become_dealer', _('I am interested in becoming a distributor.')),
        ('technical', 'I need technical support.'),
        ('other', _('Other'))
    ]
    
    help_type = models.CharField(max_length=50, choices=HELP_CHOICES, verbose_name=_('Help Type'))
    company_name = models.CharField(max_length=255, verbose_name=_('Company Name'))
    question = models.TextField(verbose_name=_('Question'))
    first_name = models.CharField(max_length=100, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=100, verbose_name=_('Last Name'))
    email = models.EmailField(verbose_name=_('Email'))
    phone_number = models.CharField(max_length=20, verbose_name=_('Phone Number'))
    
    ip_address = models.GenericIPAddressField(verbose_name=_('IP Address'), null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company_name}"

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')


class ContactInfo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    aminol_headquarters = models.TextField()
    aminol_headquarters_location = models.URLField(blank=True, help_text="URL for headquarters location (Google Maps link)")
    aminol_factory = models.TextField()
    aminol_factory_location = models.URLField(blank=True, help_text="URL for factory location (Google Maps link)")
    aminol_headquarters_image = models.ImageField(upload_to='aminol_headquarters/')
    aminol_factory_image = models.ImageField(upload_to='aminol_factory/')
    registers = models.TextField()
    contact_address = models.TextField()
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    
    def __str__(self):
        return f"{self.title}"