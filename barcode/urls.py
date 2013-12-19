from django.conf.urls import patterns, include, url


urlpatterns = patterns('barcode.views',
    url(r'^csv/(?P<type>\w+)/$', 'upload_csv'),
)
