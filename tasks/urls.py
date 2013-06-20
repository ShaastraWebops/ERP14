from django.conf.urls import patterns, include, url


urlpatterns = patterns('tasks.views',
    url(r'^add/$', 'add_intra_task'),
    url(r'^add/(?P<primkey>\d+)/$', 'add_intra_task'),
    
    url(r'^addx/$', 'add_cross_task'),
    url(r'^addx/(?P<primkey>\d+)/$', 'add_cross_task'),  
    
    url(r'^edit/(?P<primkey>\d+)/$', 'edit_task'),                    
    url(r'^display/(?P<primkey>\d+)/$', 'display_task'), 
    url(r'^del/(?P<primkey>\d+)/$', 'delete_task'), 
                                                                                   
#  url(r'^addcopy/$', 'libauth.views.AddCopy'),
# url(r'^updatecopy/(?P<primkey>\d+)/$', 'libauth.views.UpdateCopy'),
)
