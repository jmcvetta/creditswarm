# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from django import forms
from django.core.exceptions import ValidationError

from dispute.models import Dispute
from dispute.models import BadInfo
from dispute.models import Account
from dispute.models import Inquiry


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