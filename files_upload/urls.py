from django.conf.urls import patterns, include, url


urlpatterns = patterns('files_upload.views',
    
    url(r'^$', 'upload_file'),
    url(r'^list/$','list_of_spons'),
    url(r'^edit_title/(\d+)/$','edit_title'),                                                              
)
