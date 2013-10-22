from django.conf.urls import patterns, include, url


urlpatterns = patterns('files_upload.views',
    
    url(r'^$', 'upload_file'),                                                                
)
