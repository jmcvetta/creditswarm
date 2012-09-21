# Copyright (c) 2012 Jason McVetta.

from django import forms
from django.core.exceptions import ValidationError

from case.models import Case
from case.models import Account
from case.models import Inquiry
from case.models import Demographic


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        exclude = ['user', 'status', 'ts_submitted', 'ts_transmitted']


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ['case']


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        exclude = ['case']

class DemographicForm(forms.ModelForm):
    class Meta:
        model = Demographic
        exclude = ['case']