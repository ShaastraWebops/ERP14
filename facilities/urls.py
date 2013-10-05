from django.conf.urls import patterns, include, url


urlpatterns = patterns('facilities.views',
    #Facilities Home
    url(r'^home/$', 'FacilitiesHome'),
    
    #Order Management Views
    url(r'^create/$', 'CreateOrder'), 
    url(r'^approve/(?P<primkey>\d+)/$', 'ApproveOrder'),
    url(r'^delentry/(?P<primkey>\d+)/$', 'DeleteEntry'),
    url(r'^editentry/(?P<primkey>\d+)/$', 'EditEntry'),
    url(r'^delorder/(?P<primkey>\d+)/$', 'DeleteOrder'),
    
    #Add Item to Catalog
    url(r'^addmenuitem/$', 'AddMenuItem'),
    
    #Redirect to Facilites Home
    url(r'^/$', 'FacilitiesRedirect'),
    url(r'^$', 'FacilitiesRedirect'),
                                                                                   
)
