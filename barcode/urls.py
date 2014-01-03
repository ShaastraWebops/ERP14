from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('barcode.views',
    url(r'^barcode/$', 'upload_csv', {'type': "barcodeportal"}, name = "barcodeportal"),
    url(r'^participants/$', 'upload_csv', {'type': "participantsportal"}, name = "participantsportal"),
    url(r'^add_single_barcode/$','add_single_entry',{'type': "barcodeportal"},name="add_single_barcode"),
    url(r'^add_single_participant/$','add_single_entry',{'type': "participantsportal"},name="add_single_participant"),
    url(r'^get_details/(?P<sh_id>\w+)/$','get_details'),#tried to get shaastra id search query from url
    url(r'^get_details','get_details',{'sh_id':None}),
    url(r'^edit_profile/(?P<shaastra_id>\w+)/$','edit_profile'),
    url(r'^ppm/$', 'upload_ppm'),
    url(r'^direct/$', direct_to_template, {'template': 'barcode/result_announce.html'}),
    url(r'^detail_entry',direct_to_template,{'template':'barcode/detail_entry.html'},name = 'detail_entry'),
    url(r'^winners/$','hospi_announce'),
    url(r'^event_winners/(?P<event_id>\w+)/$','event_winners'),
    
)
