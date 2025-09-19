# contact/forms.py

from django import forms
from .models import Contact
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['help_type', 'company_name', 'question', 'first_name', 
                  'last_name', 'email', 'phone_number']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Etiketleri burada tanımlamak daha iyi bir pratiktir
        self.fields['help_type'].label = _("How can we help you?*")
        self.fields['company_name'].label = _("Company name*")
        self.fields['question'].label = _("Your question, wish and/or clarification*")
        self.fields['first_name'].label = _("First name*")
        self.fields['last_name'].label = _("Last name*")
        self.fields['email'].label = _("Email address*")
        self.fields['phone_number'].label = _("Phone number*")