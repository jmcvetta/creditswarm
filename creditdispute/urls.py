from django.conf.urls import patterns, include, url
from complain.views import IndexView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'creditdispute.views.home', name='home'),
    # url(r'^creditdispute/', include('creditdispute.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', IndexView.as_view()),
    #url(r'^accounts/', include(regurls)),
    url(r'^accounts/', include('allauth.urls')),
) 

urlpatterns += staticfiles_urlpatterns()
