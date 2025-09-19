from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['help_type', 'company_name', 'question', 'first_name', 
                  'last_name', 'email', 'phone_number']
        
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.required = True
            
        self.fields['help_type'].label = "How can we help you?*"
        self.fields['company_name'].label = "Company name*"
        self.fields['question'].label = "Your question, wish and/or clarification*"
        self.fields['first_name'].label = "First name*"
        self.fields['last_name'].label = "Last name*"
        self.fields['email'].label = "Email address*"
        self.fields['phone_number'].label = "Phone number*"