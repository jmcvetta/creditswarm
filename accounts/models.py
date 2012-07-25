from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.localflavor.us.us_states import US_STATES
from django.contrib.localflavor.us.models import USPostalCodeField


class UserProfile(models.Model):  
    user = models.OneToOneField(User)  
    address1 = models.CharField(max_length=255, blank=False)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=False)
    state = USPostalCodeField(blank=False)
    zip = models.CharField(max_length=5, blank=False)
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
