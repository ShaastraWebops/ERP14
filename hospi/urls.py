from django.conf.urls import patterns, include, url

urlpatterns = patterns('hospi.views',
        url(r'^$','home'),
        url(r'^checkin/$','checkin'),
        url(r'^teamcheckin/(?P<pk>\d+)/(?P<team_id>\d+)/$','teamcheckin'),
        )
