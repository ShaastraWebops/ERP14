from django.shortcuts import render_to_response, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from misc.dajaxice.core import dajaxice_functions
from finance.models import Vendor


@login_required
def home ( request ) :

    userprofile = request.user.get_profile()

    query_dictionary = {}
    query_dictionary['userprofile'] = userprofile
    
    return render_to_response ( 'finance/home.html', query_dictionary, context_instance = RequestContext ( request ) )

@login_required
def vouchers ( request ) :

    userprofile = request.user.get_profile()

    query_dictionary = {}
    query_dictionary['userprofile'] = userprofile
    query_dictionary['isfinance'] = ( userprofile.dept.name == 'Finance' )
    query_dictionary['vendors'] = Vendor.objects.all() 


    #If the user is a finance coord
    if query_dictionary['isfinance']:
	return render_to_response ('finance/voucher_fin.html', query_dictionary, context_instance = RequestContext ( request ) )

    #If the user is a gen coord
    return render_to_response ( 'finance/voucher.html', query_dictionary, context_instance = RequestContext ( request ) )


