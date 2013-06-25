from django.conf.urls import patterns, include, url
import os.path
from erp.settings import STATIC_URL
from django.views.generic.simple import redirect_to
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# For DajaxIce to work
from misc.dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'erp.views.home', name='home'),
    # url(r'^erp/', include('erp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tasks/', include('tasks.urls')),
    url(r'^login/$', 'users.views.login'),
    url(r'^/$', redirect_to, {'url': '/login/'}),
    url(r'^$', redirect_to, {'url': '/login/'}),
    url(r'^choose_identity/$', 'users.views.choose_identity'),
    url(r'^logout/$', 'users.views.logout'),
    url(r'^dash/$', 'dash.views.dash_view'),
    url(r'^users/', include('users.urls')),
    
    url(r'^comments/', include('django.contrib.comments.urls')),
    
    url(dajaxice_config.dajaxice_url, include('misc.dajaxice.urls')), # For dajaxice to function corrently
)

urlpatterns += staticfiles_urlpatterns() # To enable serving static files
