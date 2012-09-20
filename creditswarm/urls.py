# Copyright (c) 2012 Jason McVetta.

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from case.views import home_view
from case.views import LoginView
#
from case.views import CaseCreateView
from case.views import CaseDetailView
from case.views import CaseUpdateView
from case.views import CaseDeleteView
from case.views import CaseConfirmationView
#
from case.views import AccountCreateView
from case.views import AccountUpdateView
from case.views import AccountDeleteView
#
from case.views import InquiryCreateView
from case.views import InquiryUpdateView
from case.views import InquiryDeleteView
#
from case.views import DemographicCreateView
from case.views import DemographicUpdateView
from case.views import DemographicDeleteView
#
from case.views import cra_login
from case.views import CraCaseDetailView
from case.views import CraLoginView
#
from profile.views import UserProfileView


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
    # Social Auth
    #
    url(r'', include('social_auth.urls')),
    #
    # Account management
    #
    url(r'^profile/edit$', 
        UserProfileView.as_view(),
        name='profile-edit',
        ),
    #
    # Case
    #
    url(r'^case/new/$', CaseCreateView.as_view(), name='case-new'),
    url(r'^case/(?P<pk>\d+)/$', CaseDetailView.as_view(), name='case-detail'),
    url(r'^case/(?P<pk>\d+)/edit/$', CaseUpdateView.as_view(), name='case-edit'),
    url(r'^case/(?P<pk>\d+)/delete/$', CaseDeleteView.as_view(), name='case-delete'),
    url(r'^case/(?P<pk>\d+)/submit/$', CaseConfirmationView.as_view(), name='case-confirm'),
    #
    # Account
    #
    url(r'^case/(?P<case_pk>\d+)/account/new/$', AccountCreateView.as_view(), name='account-new'),
    url(r'^case/account/(?P<pk>\d+)/edit/$', AccountUpdateView.as_view(), name='account-edit'),
    url(r'^case/account/(?P<pk>\d+)/delete/$', AccountDeleteView.as_view(), name='account-delete'),
    #
    # Inquiry
    #
    url(r'^case/(?P<case_pk>\d+)/inquiry/new/$', InquiryCreateView.as_view(), name='inquiry-new'),
    url(r'^case/inquiry/(?P<pk>\d+)/edit/$', InquiryUpdateView.as_view(), name='inquiry-edit'),
    url(r'^case/inquiry/(?P<pk>\d+)/delete/$', InquiryDeleteView.as_view(), name='inquiry-delete'),
    #
    # Demographic
    #
    url(r'^case/(?P<case_pk>\d+)/demographic/new/$', DemographicCreateView.as_view(), name='demographic-new'),
    url(r'^case/demographic/(?P<pk>\d+)/edit/$', DemographicUpdateView.as_view(), name='demographic-edit'),
    url(r'^case/demographic/(?P<pk>\d+)/delete/$', DemographicDeleteView.as_view(), name='demographic-delete'),
    #
    # Credit Reporting Agency
    #
    url(r'^cra/login/$', cra_login, name='cra-login'),
    url(r'^cra/case/(?P<pk>\d+)/$', CraCaseDetailView.as_view(), name='cra-case-detail'),
)

urlpatterns += staticfiles_urlpatterns()
