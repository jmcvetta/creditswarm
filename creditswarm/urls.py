# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from dispute.views import home_view
from dispute.views import LoginView
#
from dispute.views import DisputeCreateView
from dispute.views import DisputeDetailView
from dispute.views import DisputeUpdateView
from dispute.views import DisputeDeleteView
from dispute.views import DisputeConfirmationView
#
from dispute.views import AccountCreateView
from dispute.views import AccountUpdateView
from dispute.views import AccountDeleteView
#
from dispute.views import InquiryCreateView
from dispute.views import InquiryUpdateView
from dispute.views import InquiryDeleteView
#
from profile.views import SignupView
from profile.views import SettingsView

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
    url(r"^account/signup/$", SignupView.as_view(), name="account_signup"),
    url(r"^account/settings/$", SettingsView.as_view(), name="account_settings"),
    url(r"^account/", include("account.urls")),
    #
    # Dispute
    #
    url(r'^dispute/new/$', DisputeCreateView.as_view(), name='dispute-new'),
    url(r'^dispute/(?P<pk>\d+)/$', DisputeDetailView.as_view(), name='dispute-detail'),
    url(r'^dispute/(?P<pk>\d+)/edit/$', DisputeUpdateView.as_view(), name='dispute-edit'),
    url(r'^dispute/(?P<pk>\d+)/delete/$', DisputeDeleteView.as_view(), name='dispute-delete'),
    url(r'^dispute/(?P<pk>\d+)/submit/$', DisputeConfirmationView.as_view(), name='dispute-submit'),
    #
    # Account
    #
    url(r'^dispute/(?P<dispute_pk>\d+)/account/new/$', AccountCreateView.as_view(), name='account-new'),
    url(r'^dispute/account/(?P<pk>\d+)/edit/$', AccountUpdateView.as_view(), name='account-edit'),
    url(r'^dispute/account/(?P<pk>\d+)/delete/$', AccountDeleteView.as_view(), name='account-delete'),
    #
    # Inquiry
    #
    url(r'^dispute/(?P<dispute_pk>\d+)/inquiry/new/$', InquiryCreateView.as_view(), name='inquiry-new'),
    url(r'^dispute/inquiry/(?P<pk>\d+)/edit/$', InquiryUpdateView.as_view(), name='inquiry-edit'),
    url(r'^dispute/inquiry/(?P<pk>\d+)/delete/$', InquiryDeleteView.as_view(), name='inquiry-delete'),
)

urlpatterns += staticfiles_urlpatterns()
