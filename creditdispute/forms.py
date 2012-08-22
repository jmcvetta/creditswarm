# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from django import forms
from django.forms import widgets
from django.forms.formsets import formset_factory

from creditdispute.models import CRA_CHOICES
from creditdispute.models import DETAIL_REASON_CHOICES

class CreditReportForm(forms.Form):
    cra = forms.ChoiceField(choices=CRA_CHOICES, required=True,
        label='Credit Reporting Agency')
    report_number = forms.CharField(max_length=128, required=True,
        label='Report Number')

class DetailForm(forms.Form):
    company_name = forms.CharField(max_length=128, required=True)
    account_number = forms.CharField(max_length=128, required=True)
    reason = forms.ChoiceField(choices=DETAIL_REASON_CHOICES, required=True)
    other_reason = forms.CharField(widget=widgets.Textarea, required=False)

DetailFormSet = formset_factory(DetailForm)