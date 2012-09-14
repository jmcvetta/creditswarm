# Copyright (c) 2012 Jason McVetta.

from django import forms
from django.core.exceptions import ValidationError

from dispute.models import Dispute
from dispute.models import Account
from dispute.models import Inquiry
from dispute.models import Demographic


class DisputeForm(forms.ModelForm):
    class Meta:
        model = Dispute
        exclude = ['user', 'status', 'ts_submitted']


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ['dispute']


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        exclude = ['dispute']

class DemographicForm(forms.ModelForm):
    class Meta:
        model = Demographic
        exclude = ['dispute']