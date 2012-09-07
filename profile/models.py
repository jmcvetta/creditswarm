# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
from django.contrib.localflavor.us.models import USPostalCodeField
from django.contrib.localflavor.us.models import USStateField


class UserProfile(models.Model):  
    user = models.OneToOneField(User)
    #
    # Personal Info 
    # - use encrypted fields before running in production!
    #
    family_name = models.CharField(max_length=128)
    given_name = models.CharField(max_length=128)
    ssn = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    address1 = models.CharField(max_length=128)
    address2 = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128)
    state = USStateField()
    zip = USPostalCodeField(verbose_name='Zip Code')
    home_phone = PhoneNumberField(blank=False, null=False)
    work_phone = PhoneNumberField(blank=True, null=True)
