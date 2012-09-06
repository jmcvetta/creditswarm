# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from functools import wraps

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.contrib import messages

from profile.models import UserProfile
from profile.forms import SignupForm
from profile.forms import SettingsForm


import account.views


class SettingsView(account.views.SettingsView):
    
    form_class = SettingsForm

    def update_settings(self, form):
        self.update_profile(form)
        super(SettingsView, self).update_settings(form)
    
    def update_profile(self, form):
        profile = self.request.user.get_profile()
        profile.given_name = form.cleaned_data["given_name"] 
        profile.family_name = form.cleaned_data["family_name"] 
        profile.address1 = form.cleaned_data["address1"] 
        profile.address2 = form.cleaned_data["address2"] 
        profile.city = form.cleaned_data["city"] 
        profile.state = form.cleaned_data["state"] 
        profile.zip = form.cleaned_data["zip"] 
        profile.date_of_birth = form.cleaned_data["date_of_birth"] 
        profile.ssn = form.cleaned_data["ssn"] 
        profile.save()
    
    def get_initial(self):
        initial = super(SettingsView, self).get_initial()
        profile = self.request.user.get_profile()
        initial["given_name"] = profile.given_name
        initial["family_name"] = profile.family_name
        initial["address1"] = profile.address1
        initial["address2"] = profile.address2
        initial["city"] = profile.city
        initial["state"] = profile.state
        initial["zip"] = profile.zip
        initial["date_of_birth"] = profile.date_of_birth
        initial["ssn"] = profile.ssn
        return initial

class SignupView(account.views.SignupView):

    form_class = SignupForm
    
    def after_signup(self, form):
        self.create_profile(form)
        super(SignupView, self).after_signup(form)
    
    def create_profile(self, form):
        profile = UserProfile(user=self.created_user)
        #profile.user = self.created_user
        profile.given_name = form.cleaned_data["given_name"]
        profile.family_name = form.cleaned_data["family_name"]
        profile.address1 = form.cleaned_data["address1"]
        profile.address2 = form.cleaned_data["address2"]
        profile.city = form.cleaned_data["city"]
        profile.state = form.cleaned_data["state"]
        profile.zip = form.cleaned_data["zip"]
        profile.date_of_birth = form.cleaned_data["date_of_birth"]
        profile.ssn = form.cleaned_data["ssn"]
        profile.save()
    


def profile_required(method):
    '''
    Decorator that redirects user to profile creation page if they 
    do not have a user profile.
    '''
    @wraps(method)
    def wrapper(request, *args, **kwargs):
        try:
            request.user.get_profile()
        except UserProfile.DoesNotExist:
            
            messages.add_message(request, messages.INFO, 'Hello world.')
            return HttpResponseRedirect(reverse('edit_profile'))
        return method(request, *args, **kwargs)
    return wrapper


#class UserProfileView(UpdateView):
#    '''
#    Edit profile for current user.
#    '''
#    model = UserProfile
#    form_class = UserProfileForm
#    success_url = '/'
#    
#    def get_initial(self):
#        '''
#        If user does not already have a profile, then populate form intial 
#        values with given and family names from User object.
#        '''
#        initial = self.initial
#        if not UserProfile.objects.filter(user=self.request.user):
#            initial['given_name'] = self.request.user.first_name
#            initial['family_name'] = self.request.user.last_name
#        return initial
#
#    
#    def get_object(self, queryset=None):
#        try:
#            return UserProfile.objects.get(user=self.request.user)
#        except UserProfile.DoesNotExist:
#            return None
#
#    
#    def form_valid(self, form):
#        form.instance.user = self.request.user
#        return super(UserProfileView, self).form_valid(form)
