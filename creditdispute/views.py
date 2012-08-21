from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.shortcuts import render

class LoginView(TemplateView):
    template_name = 'login.html'

def home_view(request):
    if request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        return render(request, 'landing.html')