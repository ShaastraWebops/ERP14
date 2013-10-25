from django.conf.urls import patterns, include, url


urlpatterns = patterns('finance.views',
    
    url(r'^$', 'home'),                    
    url(r'^vouchers/$', 'vouchers'),
    
    ##BUDGETING
    url(r'^budgeting/$', 'budgeting'),
    url(r'^createbudget/$', 'create_budget'),
    url(r'^approvebudget/(?P<primkey>\d+)/(?P<option>\d+)/$', 'approve_budget'),
    url(r'^viewbudget/(?P<primkey>\d+)/$', 'budget_page'),
    
    #PAYMENTS
    url(r'^addpayment/$', 'add_payment_request'),
    url(r'^viewpayment/(?P<primkey>\d+)/$', 'payment_page'),
    url(r'^payments/$', 'payments'),
    url(r'^approvepayment/(?P<primkey>\d+)/$', 'approve_payment'),
    
    #VOUCHERS
    url(r'^addvoucher/(?P<vendorid>\d+)/$', 'add_voucher_request'),
    url(r'^vouchers/$', 'vouchers'),
    url(r'^vouchers/(?P<vendorid>\d+)/$', 'vouchers'),
    url(r'^viewvoucher/(?P<primkey>\d+)/$', 'voucher_page'),
    url(r'^approvevoucher/(?P<primkey>\d+)/$', 'approve_voucher'),

    #ADVANCES
    url(r'^addadvance/$', 'add_advance_request'),
    url(r'^viewadvance/(?P<primkey>\d+)/$', 'advance_page'),
    url(r'^advances/$', 'advances'),
    url(r'^approveadvance/(?P<primkey>\d+)/$', 'approve_advance'),
                                                                                   
)
