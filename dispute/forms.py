# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from django import forms
from django.forms import widgets
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory

from dispute.models import CRA_CHOICES
from dispute.models import DETAIL_REASON_CHOICES
from dispute.models import Dispute
from dispute.models import BadInfo
from dispute.models import Detail
from dispute.models import Inquiry

class DisputeForm(forms.ModelForm):
    class Meta:
        model = Dispute
        exclude = ['user', 'status']

class DetailForm(forms.ModelForm):
    class Meta:
        model = Detail
        exclude = ['dispute']
