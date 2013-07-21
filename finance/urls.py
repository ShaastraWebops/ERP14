from django.conf.urls import patterns, include, url


urlpatterns = patterns('finance.views',
    
    url(r'^$', 'home'),                    
    url(r'^vouchers/$', 'vouchers'),
                                                                                   
)
