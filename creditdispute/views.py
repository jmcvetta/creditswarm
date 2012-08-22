# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from django.views.generic import TemplateView
from django.views.generic import ListView
#from django.shortcuts import render_to_response
from django.shortcuts import render
from creditdispute.models import Dispute

class LoginView(TemplateView):
    template_name = 'login.html'

def home_view(request):
    if request.user.is_authenticated():
        #return render(request, 'home.html')
        return DisputeListView.as_view()(request)
    else:
        return render(request, 'landing.html')

class DisputeListView(ListView):
    model = Dispute
    
    def get_queryset(self):
        return Dispute.objects.filter(user=self.request.user)