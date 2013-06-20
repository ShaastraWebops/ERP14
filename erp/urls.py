from django.conf.urls import patterns, include, url
import os.path
from erp.settings import STATIC_URL

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
    url(r'^choose_identity/$', 'users.views.choose_identity'),
    url(r'^logout/$', 'users.views.logout'),
    url(r'^dash/$', 'dash.views.dash_view'),
    url(r'^users/', include('users.urls')),
    
    (r'^comments/', include('django.contrib.comments.urls')),
    
    (dajaxice_config.dajaxice_url, include('dajaxice.urls')), # For dajaxice to function corrently
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {   'document_root' : STATIC_URL } ), # For static files to be server properly (on server)
            
    
)
