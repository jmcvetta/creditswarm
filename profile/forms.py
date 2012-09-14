# Copyright (c) 2012 Jason McVetta.

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.localflavor.us.forms import USSocialSecurityNumberField
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.contrib.localflavor.us.forms import USStateSelect
from django.contrib.localflavor.us.forms import USStateField
from django.contrib.localflavor.us.forms import USZipCodeField


from profile.models import UserProfile


class UserProfileForm(forms.ModelForm):
    state = USStateField(widget=USStateSelect)
    zip = USZipCodeField(label='Zip Code')
    phone = USPhoneNumberField(label='Home Phone Number')
    ssn = USSocialSecurityNumberField(label='Social Security Number', 
        help_text='SSN is required by credit reporting agencies.')

    class Meta:
        model = UserProfile
        exclude = ['user']