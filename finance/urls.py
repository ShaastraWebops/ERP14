from django.conf.urls import patterns, include, url


urlpatterns = patterns('finance.views',
    
    url(r'^$', 'home'),                    
    url(r'^vouchers/$', 'vouchers'),
    
    ##BUDGETING
    url(r'^budgeting/$', 'finance_budget_portal'),
    url(r'^createbudget/$', 'create_budget'),
    url(r'^approvebudget/(?P<primkey>\d+)/(?P<option>\d+)/$', 'approve_budget'),
    url(r'^viewbudget/(?P<primkey>\d+)/$', 'budget_page'),
                                                                                   
)
