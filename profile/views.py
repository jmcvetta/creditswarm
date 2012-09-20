# Copyright (c) 2012 Jason McVetta.

from functools import wraps

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.contrib import messages

from profile.models import UserProfile
from profile.forms import UserProfileForm


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


class UserProfileView(UpdateView):
    '''
    Edit profile for current user.
    '''
    model = UserProfile
    form_class = UserProfileForm
    success_url = '/'
    
    def get_initial(self):
        '''
        If user does not already have a profile, then populate form intial 
        values with given and family names from User object.
        '''
        initial = self.initial
        if not UserProfile.objects.filter(user=self.request.user):
            initial['given_name'] = self.request.user.first_name
            initial['family_name'] = self.request.user.last_name
        return initial

    
    def get_object(self, queryset=None):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            return None

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:
            return next_url
        else:
            return super(UserProfileView, self).get_success_url()

    
    def form_valid(self, form):
        form.instance.user = self.request.user
        self.request.user.first_name = form.instance.given_name
        self.request.user.last_name = form.instance.family_name
        self.request.user.save()
        return super(UserProfileView, self).form_valid(form)