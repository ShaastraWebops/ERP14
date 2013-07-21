from django.shortcuts import render_to_response, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from misc.dajaxice.core import dajaxice_functions


@login_required
def home ( request ) :

    userprofile = request.user.get_profile()

    query_dictionary = {}
    query_dictionary['userprofile'] = userprofile
    
    return render_to_response ( 'finance/home.html', query_dictionary, context_instance = RequestContext ( request ) )

def vouchers ( request ) :

    userprofile = request.user.get_profile()

    query_dictionary = {}
    query_dictionary['userprofile'] = userprofile

    return render_to_response ( 'finance/voucher.html', query_dictionary, context_instance = RequestContext ( request ) )


