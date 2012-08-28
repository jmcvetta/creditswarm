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

from dispute.models import Dispute
from dispute.models import Detail
from dispute.forms import DisputeForm
from dispute.forms import DetailForm


#-------------------------------------------------------------------------------
#
# Mixins & Exceptions
#
#-------------------------------------------------------------------------------

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

           
#-------------------------------------------------------------------------------
#
# Home & Account Views
#
#-------------------------------------------------------------------------------

class LoginView(TemplateView):
    template_name = 'login.html'

def home_view(request):
    if request.user.is_authenticated():
        #return render(request, 'home.html')
        return DisputeListView.as_view()(request)
    else:
        return render(request, 'landing.html')

#-------------------------------------------------------------------------------
#
# Dispute Views
#
#-------------------------------------------------------------------------------

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


#-------------------------------------------------------------------------------
#
# Detail Views
#
#-------------------------------------------------------------------------------

class DetailCreateView(CreateView):
    model = Detail
    form_class = DetailForm
    
    def form_valid(self, form):
        dispute_pk = self.kwargs.get('dispute_pk', None)
        d = Dispute.objects.get(pk=dispute_pk)
        form.instance.dispute = d
        return super(DetailCreateView, self).form_valid(form)
    
    def get_success_url(self):
        dispute_pk = self.kwargs.get('dispute_pk', None)
        return reverse('dispute-detail', kwargs={'pk': dispute_pk})

class DetailUpdateView(UpdateView):
    model = Detail
    form_class = DetailForm
    
    def get_success_url(self):
        dispute_pk = self.get_object().dispute.pk
        return reverse('dispute-detail', kwargs={'pk': dispute_pk})
    
class DetailDeleteView(DeleteView):
    model = Detail
    
    def get_success_url(self):
        dispute_pk = self.get_object().dispute.pk
        return reverse('dispute-detail', kwargs={'pk': dispute_pk})
    

def detail_create(request, dispute_pk):
    pass
