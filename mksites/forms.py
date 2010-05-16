from django.contrib.auth.forms import UserCreationForm
from django import forms
from subdomains.models import Subdomain

class SubdomainUserForm(UserCreationForm):
    subdomain_title = forms.CharField(max_length=50,label='Site name')
    
    def clean(self):
        subdomain_value = self.cleaned_data['username']
        if subdomain_value=='www':
            raise forms.ValidationError('This Subdomain cannot be registered')
        try:
            Subdomain.objects.get(subdomain_text=subdomain_value)
        except Subdomain.DoesNotExist:
            return self.cleaned_data
        raise forms.ValidationError('This Subdomain cannot be registered')
    
    def save(self,**kwargs):
        user = super(SubdomainUserForm,self).save(**kwargs)
        cd =self.cleaned_data
        username,password = cd['username'],cd['password2']
        subdomain = Subdomain.objects.register_new_subdomain(subdomain_text = cd['username'],
                                                             name=cd['subdomain_title'],
                                                             description = "Descriptions",
                                                             user = user)
        return username,password,subdomain