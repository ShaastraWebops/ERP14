from django.conf.urls import patterns, include, url

urlpatterns = patterns('users.views',

	url(r'^view_profile/$', 'view_profile' ),
	url(r'^view_profile/(?P<userid>\w+)/$','view_profile'),
	url(r'^edit_profile/$', 'edit_profile' ),
)
