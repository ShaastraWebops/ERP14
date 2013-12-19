from django.conf.urls import patterns, include, url


urlpatterns = patterns('barcode.views',
    url(r'^csv/barcode/$', 'upload_csv', {'type': "barcodeportal"}, name = "barcodeportal"),
    url(r'^csv/participants/$', 'upload_csv', {'type': "participantsportal"}, name = "participantsportal"),
)
