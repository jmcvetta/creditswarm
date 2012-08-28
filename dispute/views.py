# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.core.urlresolvers import reverse
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib import messages

from accounts.models import UserProfile
from accounts.forms import UserProfileForm
from dispute.models import Dispute
from dispute.forms import DisputeForm
from dispute.forms import CreditReportFormSet
from dispute.forms import DetailFormSet


class OwnershipError(RuntimeError):
    '''
    You do not own the requested object.
    '''

class StatusError(RuntimeError):
    '''
    Wrong status for requested action.
    '''


class OwnedSingleObjectMixin(object):
    '''
    Overrides SingleObjectMixin.get_object() to ensure the current user owns
    the requested object.
    '''
    
    def get_object(self, queryset=None):
        obj = super(OwnedSingleObjectMixin, self).get_object(queryset=queryset)
        if obj.user == self.request.user:
            return obj
        else:
            raise OwnershipError('You do not own the requested object.')

class DraftMixin(OwnedSingleObjectMixin):
    '''
    '''
    def get_object(self, queryset=None):
        obj = super(DraftMixin, self).get_object(queryset=queryset)
        if not obj.status == 'D':
            raise StatusError('Requested action can only be performed on objects with Draft status.')
        return obj
           

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

class DisputeCreateView(CreateView):
    model = Dispute
    form_class = DisputeForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(DisputeCreateView, self).form_valid(form)


class DisputeDetailView(OwnedSingleObjectMixin, DetailView):
    model = Dispute


class DisputeUpdateView(DraftMixin, UpdateView):
    model = Dispute
    form_class = DisputeForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(DisputeUpdateView, self).form_valid(form)


class DisputeDeleteView(DraftMixin, DeleteView):
    model = Dispute
    success_url = '/'


def dispute_submit(request, pk):
    d = get_object_or_404(Dispute, pk=pk)
    if not d.user == request.user:
        raise OwnershipError('You do not own the requested object.')
    if not d.status == 'D':
        raise RuntimeError('Can only submit disputes that are in Draft status.')
    d.status = 'Q' # Queued for send
    d.save()
    messages.add_message(request, messages.INFO, 'Dispute #%s was queued for submission.' % d.pk)
    return HttpResponseRedirect(reverse('home'))


class DisputeWizard(SessionWizardView):
    
    template_name = 'dispute/dispute_wizard.html'
    
    def done(self, form_list, **kwargs):
        #do_something_with_the_form_data(form_list)
        for form in form_list:
            print form.cleaned_data # FIXME: this is useless debug output
        return HttpResponseRedirect('/') # FIXME: redirect somewhere sensible
    

def dispute_wizard_view(request):
    instance_dict = {}
    try:
        profile = request.user.get_profile()
        instance_dict[0] = profile
    except UserProfile.DoesNotExist:
        pass
    print instance_dict
    return DisputeWizard.as_view(
        [
            UserProfileForm,
            DisputeForm,
            CreditReportFormSet,
            DetailFormSet,
            ],
        instance_dict = instance_dict,
        )(request)