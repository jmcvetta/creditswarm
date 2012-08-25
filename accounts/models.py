# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from functools import wraps

from django.db import models
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class UserProfile(models.Model):  
    user = models.OneToOneField(User)
    #
    # Personal Info 
    # - use encrypted fields before running in production!
    #
    given_name = models.CharField(max_length=128)
    family_name = models.CharField(max_length=128)
    address1 = models.CharField(max_length=128, verbose_name='Address 1')
    address2 = models.CharField(max_length=128, null=True, blank=True, verbose_name="Address 2")
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    zip = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    ssn = models.CharField(max_length=128)

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
            return HttpResponseRedirect(reverse('new_profile'))
        return method(request, *args, **kwargs)
    return wrapper