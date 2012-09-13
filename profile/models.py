# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
from django.contrib.localflavor.us.models import USStateField



class UserProfile(models.Model):  
    user = models.OneToOneField(User)
    #
    # Personal Info 
    # - use encrypted fields before running in production!
    #
    given_name = models.CharField(max_length=128, verbose_name='First Name')
    family_name = models.CharField(max_length=128, verbose_name='Last Name')
    address1 = models.CharField(max_length=128, verbose_name='Address 1')
    address2 = models.CharField(max_length=128, null=True, blank=True, verbose_name="Address 2")
    city = models.CharField(max_length=128)
    state = USStateField()
    zip = models.CharField(max_length=128, verbose_name='Zip Code')
    date_of_birth = models.DateField(verbose_name='Date of Birth')
    ssn = models.CharField(max_length=128, verbose_name='Social Security Number')
    phone = PhoneNumberField(blank=False, null=False, verbose_name='Primary Phone Number')
