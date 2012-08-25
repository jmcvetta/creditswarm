# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.contrib.formtools.wizard.views import SessionWizardView

from dispute.models import Dispute
from dispute.forms import CreditReportForm
from dispute.forms import DetailFormSet


class LoginView(TemplateView):
    template_name = 'login.html'

def home_view(request):
    if request.user.is_authenticated():
        #return render(request, 'home.html')
        return DisputeListView.as_view()(request)
    else:
        return render(request, 'landing.html')

class DisputeListView(ListView):
    model = Dispute
    template_name = 'home.html'
    
    def get_queryset(self):
        return Dispute.objects.filter(user=self.request.user)


class DisputeWizard(SessionWizardView):
    
    template_name = 'dispute/dispute_wizard.html'
    
    def done(self, form_list, **kwargs):
        #do_something_with_the_form_data(form_list)
        for form in form_list:
            print form.cleaned_data # FIXME: this is useless debug output
        return HttpResponseRedirect('/') # FIXME: redirect somewhere sensible

dispute_wizard_view = DisputeWizard.as_view([
    CreditReportForm,
    DetailFormSet,
    ])