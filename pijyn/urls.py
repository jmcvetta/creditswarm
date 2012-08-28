# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from accounts.models import UserProfile
from accounts.views import UserProfileView
#from accounts.views import profile_required
from dispute.views import LoginView
from dispute.views import DisputeCreateView
from dispute.views import DisputeDetailView
from dispute.views import DisputeUpdateView
from dispute.views import DisputeDeleteView
from dispute.views import dispute_submit
from dispute.views import home_view
#from dispute.views import dispute_wizard_view

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pijyn.views.home', name='home'),
    # url(r'^pijyn/', include('pijyn.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url(r'^$', home_view, name='home'),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', 
        'django.contrib.auth.views.logout', 
        { 'next_page': '/' },
        name='logout',
        ),
    #
    # Account management
    #
	url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile/edit$', 
        UserProfileView.as_view(),
        name='profile-edit',
        ),
    #
    # 'dispute' module
    #
    url(r'^dispute/new/$', DisputeCreateView.as_view(), name='dispute-new'),
    url(r'^dispute/(?P<pk>\d+)/$', DisputeDetailView.as_view(), name='dispute-detail'),
    url(r'^dispute/(?P<pk>\d+)/edit/$', DisputeUpdateView.as_view(), name='dispute-edit'),
    url(r'^dispute/(?P<pk>\d+)/delete/$', DisputeDeleteView.as_view(), name='dispute-delete'),
    url(r'^dispute/(?P<pk>\d+)/submit/$', dispute_submit, name='dispute-submit'),
)

urlpatterns += staticfiles_urlpatterns()
