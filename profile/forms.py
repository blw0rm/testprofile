# -*- coding: utf-8 -*-
from django import forms
from models import UserProfile
from django.contrib.admin import widgets
#from django.forms.extras.widgets import SelectDateWidget

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    birthday = forms.DateTimeField(required=False, widget=widgets.AdminDateWidget())
    contacts = forms.EmailField()
        
    def save(self, commit=True):
        self.instance.user.first_name = self.cleaned_data['first_name']
        self.instance.user.last_name = self.cleaned_data['last_name']
        self.instance.user.email = self.cleaned_data['contacts']
        self.instance.user.save()
        super(UserProfileForm, self).save(commit)
        
    class Meta:
        model = UserProfile
        exclude = ['user',]
        fields = ['first_name', 'last_name', 'birthday', 'biography', 'contacts']
        fields.reverse()
        
        
    