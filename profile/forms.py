# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.localflavor.us.forms import USSocialSecurityNumberField
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.contrib.localflavor.us.forms import USStateSelect
from django.contrib.localflavor.us.forms import USStateField
from django.contrib.localflavor.us.forms import USZipCodeField

#
import account.forms
from profile.models import UserProfile

class BaseUserForm(forms.Form):
    given_name = forms.CharField(max_length=128, label='First Name')
    family_name = forms.CharField(max_length=128, label='Last Name')
    ssn = forms.CharField(max_length=128, label='Social Security Number')
    date_of_birth = forms.DateField(label='Date of Birth')
    address1 = forms.CharField(max_length=128, label='Address 1')
    address2 = forms.CharField(max_length=128, required=False, label="Address 2")
    city = forms.CharField(max_length=128)
    state = USStateField(widget=USStateSelect)
    zip = USZipCodeField(label='Zip Code')
    home_phone = USPhoneNumberField(label='Home Phone Number')
    work_phone = USPhoneNumberField(label='Work Phone Number', required=False)

class SettingsForm(account.forms.SettingsForm, BaseUserForm):
    pass

class SignupForm(account.forms.SignupForm, BaseUserForm):
    pass

class OldUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']