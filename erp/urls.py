from django.conf.urls import patterns, include, url
import os.path
from erp.settings import STATIC_URL
from django.views.generic.simple import redirect_to

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
    
    #Password Reset Handling
    url(r'^users/password/reset/$', 'django.contrib.auth.views.password_reset',  {'post_reset_redirect' : '/users/password/reset/done/', 'template_name': 'users/password_reset_form.html'}, name="password_reset"),
    url(r'^users/password/reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'users/password_reset_done.html'}),
    url(r'^users/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',  'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect' : '/users/password/done/', 'template_name': 'users/password_reset_confirm.html'}),
    url(r'^users/password/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'users/password_reset_complete.html'}),    
    
    (r'^comments/', include('django.contrib.comments.urls')),
    
    (dajaxice_config.dajaxice_url, include('dajaxice.urls')), # For dajaxice to function corrently
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {   'document_root' : STATIC_URL } ), # For static files to be server properly (on server)
            
    
)

