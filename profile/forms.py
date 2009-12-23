# -*- coding: utf-8 -*-
from django import forms
from models import UserProfile

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    contacts = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['contacts'].initial = self.instance.user.email
        try:
            profile = self.instance.get_profile()
            self.fields['birthday'].initial = profile.birthday
            self.fields['biography'].initial = profile.biography
        except:
            pass
    
    def save(self, commit=True):
        self.instance.user.first_name = self.cleaned_data['first_name']
        self.instance.user.last_name = self.cleaned_data['last_name']
        self.instance.save()
        super(UserProfileForm, self).save(commit)
        
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'birthday', 'biography', 'contacts']
    