# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.localflavor.us.us_states import US_STATES
from django.contrib.localflavor.us.models import USPostalCodeField


class UserProfile(models.Model):  
    user = models.OneToOneField(User)
    #
    # Personal Info 
    # - use encrypted fields before running in production!
    #
    given_name = models.CharField(max_length=128)
    family_name = models.CharField(max_length=128)
    address1 = models.CharField(max_length=128)
    address2 = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    zip = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    ssn = models.CharField(max_length=128)