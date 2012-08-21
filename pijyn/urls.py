from django.conf.urls import patterns, include, url
from complain.views import IndexView, LoginView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pijyn.views.home', name='home'),
    # url(r'^pijyn/', include('pijyn.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url(r'^$', IndexView.as_view()),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', 
        'django.contrib.auth.views.logout', 
        #{'template_name': 'accounts/logged_out.html'}
        {'template_name': 'index.html'},
        name='logout',
        ),
	url(r'^accounts/', include('registration.backends.default.urls')),

)

urlpatterns += staticfiles_urlpatterns()
