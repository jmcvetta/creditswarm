# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

import datetime
#
from django.utils import timezone
from django.utils.decorators import method_decorator
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
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
#
from creditswarm import settings
#
from case.models import Case
from case.models import Account
from case.models import Inquiry
from case.models import Demographic
from case.forms import CaseForm
from case.forms import AccountForm
from case.forms import InquiryForm
from case.forms import DemographicForm
from case.tasks import SendDisputeEmailTask
#
from profile.models import UserProfile


#-------------------------------------------------------------------------------
#
# Mixins, Generic Views, & Exceptions
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

class ProtectedView(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)



class OwnedSingleObjectMixin(ProtectedView):
    '''
    Overrides SingleObjectMixin.get_object() to ensure the current user owns
    the requested object.
    '''
    
    def get_object(self, queryset=None):
        obj = super(OwnedSingleObjectMixin, self).get_object(queryset=queryset)
        if hasattr(obj, 'user'):
            user = obj.user
        elif hasattr(obj, 'case'):
            user = obj.case.user
        else:
            user = None # WTF?
        if user == self.request.user:
            return obj
        else:
            raise OwnershipError('You do not own the requested object.')

class DraftMixin(OwnedSingleObjectMixin):
    '''
    '''
    def get_object(self, queryset=None):
        obj = super(DraftMixin, self).get_object(queryset=queryset)
        if hasattr(obj, 'status'):
            status = obj.status
        elif hasattr(obj, 'case'):
            status = obj.case.status
        else:
            status = None # WTF?
        if not status == 'D':
            raise StatusError('Requested action can only be performed on objects with Draft status.')
        return obj

class CaseChildCreateView(ProtectedView, CreateView):
    
    def __get_case_from_kwargs(self):
        case_pk = self.kwargs.get('case_pk', None)
        return Case.objects.get(pk=case_pk)
    
    def get(self, request, *args, **kwargs):
        c = self.__get_case_from_kwargs()
        if not c.user == self.request.user:
            raise OwnershipError('You do not own the requested object.')
        if not c.status == 'D':
            raise StatusError('Requested action can only be performed on objects with Draft status.')
        return super(CaseChildCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        c = self.__get_case_from_kwargs()
        if not c.user == self.request.user:
            raise OwnershipError('You do not own the requested object.')
        if not c.status == 'D':
            raise StatusError('Requested action can only be performed on objects with Draft status.')
        return super(CaseChildCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.case = self.__get_case_from_kwargs()
        return super(CaseChildCreateView, self).form_valid(form)
    
    def get_success_url(self):
        case_pk = self.kwargs.get('case_pk', None)
        return reverse('case-detail', kwargs={'pk': case_pk})


class CaseChildUpdateView(DraftMixin, UpdateView):
    
    def get_success_url(self):
        case_pk = self.get_object().case.pk
        return reverse('case-detail', kwargs={'pk': case_pk})
    
class CaseChildDeleteView(DraftMixin, DeleteView):
    
    def delete(self, request, *args, **kwargs):
        case_pk = self.get_object().case.pk
        self.success_url = reverse('case-detail', kwargs={'pk': case_pk})
        return super(CaseChildDeleteView, self).delete(request, *args, **kwargs)

           
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
        return HomeTemplateView.as_view()(request)
    else:
        return render(request, 'landing.html')

#-------------------------------------------------------------------------------
#
# Case Views
#
#-------------------------------------------------------------------------------

class HomeTemplateView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        cases = Case.objects.filter(user=self.request.user)
        context['draft_cases'] = cases.filter(status='D')
        context['sent_cases'] = cases.exclude(status='D')
        return context


class CaseListView(ListView):
    model = Case
    template_name = 'home.html'
    
    def get_queryset(self):
        return Case.objects.filter(user=self.request.user)


class CaseCreateView(ProtectedView, CreateView):
    model = Case
    form_class = CaseForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CaseCreateView, self).form_valid(form)


class CaseDetailView(OwnedSingleObjectMixin, DetailView):
    model = Case


class CaseUpdateView(DraftMixin, UpdateView):
    model = Case
    form_class = CaseForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CaseUpdateView, self).form_valid(form)


class CaseDeleteView(DraftMixin, DeleteView):
    model = Case
    success_url = '/'


class CaseConfirmationView(OwnedSingleObjectMixin, DetailView):
    '''
    When called with GET, display a summary of the case to be submitted
        and a confirm button.
    When called with POST via confirm button, actually submit the case.
    '''
    
    model = Case
    template_name_suffix = '_confirmation'
    
    def get(self, request, *args, **kwargs):
        try:
            request.user.get_profile()
            return super(CaseConfirmationView, self).get(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            messages.add_message(request, messages.INFO, 'You must complete your profile before submitting a case.')
            pk = self.kwargs.get(self.pk_url_kwarg, None)
            redirect = reverse('case-confirm', args=[pk])
            url = '%s?next=%s' % (reverse('profile-edit'), redirect)
            return HttpResponseRedirect(url)
    
    
    def submit(self, request, *args, **kwargs):
        case_obj = self.get_object()
        case_obj.status = 'Q' # Queued for send
        case_obj.ts_submitted = timezone.now()
        case_obj.save()
        if settings.CELERY_ENABLED:
            SendDisputeEmailTask.delay(case_obj)
        else:
            case_obj.email_cra()
        messages.add_message(request, messages.INFO, 'Case %s has been submitted.' % case_obj.case_number)
        return HttpResponseRedirect(reverse('home'))
    
    def post(self, *args, **kwargs):
        return self.submit(*args, **kwargs)
    

#-------------------------------------------------------------------------------
#
# Account Views
#
#-------------------------------------------------------------------------------

class AccountCreateView(CaseChildCreateView):
    model = Account
    form_class = AccountForm

class AccountUpdateView(CaseChildUpdateView):
    model = Account
    form_class = AccountForm
    
class AccountDeleteView(CaseChildDeleteView):
    model = Account

#-------------------------------------------------------------------------------
#
# Inquiry Views
#
#-------------------------------------------------------------------------------

class InquiryCreateView(CaseChildCreateView):
    model = Inquiry
    form_class = InquiryForm

class InquiryUpdateView(CaseChildUpdateView):
    model = Inquiry
    form_class = InquiryForm
    
class InquiryDeleteView(CaseChildDeleteView):
    model = Inquiry


#-------------------------------------------------------------------------------
#
# Demographic Views
#
#-------------------------------------------------------------------------------

class DemographicCreateView(CaseChildCreateView):
    model = Demographic
    form_class = DemographicForm

class DemographicUpdateView(CaseChildUpdateView):
    model = Demographic
    form_class = DemographicForm
    
class DemographicDeleteView(CaseChildDeleteView):
    model = Demographic


#-------------------------------------------------------------------------------
#
# Credtt Reporting Agency Views
#
#-------------------------------------------------------------------------------

class CraLoginView(TemplateView):
    template_name = 'cra_login.html'

def cra_login(request, *args, **kwargs):
    #return login(request, *args, **kwargs, template_name='cra_login.html')
    return login(request, *args, template_name='cra_login.html', **kwargs)

class CraCaseDetailView(DetailView):
    model = Case
    #template_name_suffix = '_cra_detail'
    
    def get(self, request, *args, **kwargs):
        if self.get_object().status == 'D':
            raise StatusError('Requested action cannot be performed on objects with Draft status.')
        return super(CraCaseDetailView, self).get(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('case.cra_view'):
            msg = 'You must login with a Credit Reporting Agency account to access this resource.'
            messages.add_message(request, messages.INFO, msg)
            url = '%s?next=%s' % (reverse('cra-login'), request.path)
            return HttpResponseRedirect(url)
        return super(CraCaseDetailView, self).dispatch(request, *args, **kwargs)