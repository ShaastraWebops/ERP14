from django.conf.urls import patterns, include, url

urlpatterns = patterns('hospi.views',
        url(r'^$','home'),
        )
