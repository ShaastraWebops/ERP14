from django.conf.urls import patterns, include, url


urlpatterns = patterns('events.views',
    url(r'^$', 'home'),
    url(r'^edit/$', 'edit_event'),
    url(r'^update/$','add_update'),
    url(r'^upload/$','upload_file'),
)
