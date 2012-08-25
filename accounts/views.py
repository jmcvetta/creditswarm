from django.forms import ModelForm
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.contrib.localflavor.us.forms import USSocialSecurityNumberField
from django.contrib.localflavor.us.forms import USStateField
from django.contrib.localflavor.us.forms import USStateSelect
from django.contrib.localflavor.us.forms import USZipCodeField

from accounts.models import UserProfile


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
    
    ssn = USSocialSecurityNumberField(required=True)
    state = USStateField(required=True, widget=USStateSelect)
    zip = USZipCodeField(required=False)

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

    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserProfileView, self).form_valid(form)