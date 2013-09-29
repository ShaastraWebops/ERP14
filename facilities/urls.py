from django.conf.urls import patterns, include, url


urlpatterns = patterns('facilities.views',
    #Facilities Home
    url(r'^home/$', 'FacilitiesHome'),
    
    #Page to create an order
    url(r'^create/$', 'CreateOrder'),
    
    #View to clear an order 
    url(r'^approve/(?P<primkey>\d+)/$', 'ApproveOrder'),
    
    #Add Item to Catalog
    url(r'^addmenuitem/$', 'AddMenuItem'),
    
    #Redirect to Facilites Home
    url(r'^/$', 'FacilitiesRedirect'),
    url(r'^$', 'FacilitiesRedirect'),
                                                                                   
)
