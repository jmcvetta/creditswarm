# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.localflavor.us.us_states import US_STATES
from django.contrib.localflavor.us.models import USPostalCodeField


class UserProfile(models.Model):  
    #
    # Personal Info 
    # - use encrypted fields before running in production!
    #
    given_name = models.CharField(max_length=128, blank=False)
    family_name = models.CharField(max_length=128, blank=False)
    address1 = models.CharField(max_length=128, blank=False)
    address2 = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=False)
    state = models.CharField(max_length=128, blank=False)
    zip = models.CharField(max_length=128, blank=False)
    date_of_birth = models.DateField(blank=False)
    ssn = models.CharField(max_length=128, blank=False)
    
# Do we really want to handle profile creation with a signal?  Will that even
# work with mandatory fields?
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
