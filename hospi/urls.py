from django.conf.urls import patterns, include, url

urlpatterns = patterns('hospi.views',
        url(r'^$','home'),
        url(r'^checkin/$','checkin'),
        url(r'^bill/(?P<sid>\d+)/$','generate_bill'),
        )
