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
    url(r'^events/', include('events.urls')),
    url(r'^login/$', 'users.views.login'),
    url(r'^/$', 'users.views.redirectToLogin'),#redirect_to, {'url': '/login/'}),
    url(r'^$', 'users.views.redirectToLogin'),#redirect_to, {'url': '/login/'}),
    url(r'^choose_identity/$', 'users.views.choose_identity'),
    url(r'^logout/$', 'users.views.logout'),
    url(r'^dash/$', 'dash.views.dash_view'),
    url(r'^finance/', include('finance.urls')),
    url(r'^users/', include('users.urls')),
    
    #Password Reset Handling
    url(r'^forgotpassword/reset/$', 'django.contrib.auth.views.password_reset',  {'post_reset_redirect' : '/forgotpassword/reset/done/', 'template_name': 'users/password_reset_form.html', 'email_template_name': 'user/password_email_template.html'}, name="password_reset"),
    url(r'^forgotpassword/reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'users/password_reset_done.html'}),
    url(r'^forgotpassword/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',  'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect' : '/forgotpassword/done/', 'template_name': 'users/password_reset_confirm.html'}),
    url(r'^forgotpassword/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'users/password_reset_complete.html'}),    
    
    #Password Change
    url(r'^users/changepassword/$',  'django.contrib.auth.views.password_change', {'post_change_redirect' : '/users/changepassword/success/', 'template_name': 'users/password_change_form.html'}),    
    url(r'^users/changepassword/success/$',  'django.contrib.auth.views.password_change_done', {'template_name': 'users/password_change_done.html'}),    
    
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(dajaxice_config.dajaxice_url, include('misc.dajaxice.urls')), # For dajaxice to function corrently
)

urlpatterns += staticfiles_urlpatterns() # To enable serving static files
