#For simple dajax(ice) functionalities
from django.utils import simplejson
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
from misc.dajaxice.utils import deserialize_form

# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string

#Decorators
from django.contrib.auth.decorators import login_required, user_passes_test

#Models
from finance.models import VoucherRequest

@dajaxice_register
def budgeting_modal(request):
    """
        Used to populate the Modal with Budgeting page
    """
    dajax = Dajax()
    
    html_content = render_to_string("finance/budgeting.html", locals(), RequestContext(request))
    dajax.remove_css_class('#id_modal', 'hide') # Show modal
    dajax.assign("#id_modal", "innerHTML", html_content) # Populate modal
    
    return dajax.json()
 
@dajaxice_register
@login_required
def user_voucher_history(request, curr_vendor):
    """
	Used to display a user's history with a particular vendor
    """
    dajax = Dajax()

    userprofile = request.user.get_profile()
    query_dictionary = {}
    query_dictionary['approved_vouchers'] = VoucherRequest.objects.filter(creator=userprofile).all()
#    query_dictionary['pending_vouchers'] = VoucherRequest.objects.filter(creator=userprofile).filter(vendor.name=curr_vendor).filter(status='P').all()
    html_content = render_to_string('finance/voucher_history.html', query_dictionary, context_instance = RequestContext(request) )

    if html_content != "": 
        # put html generated above into json if not null
        # if null, alert has already been taken care of
        dajax.assign('#id_content_right','innerHTML', html_content)

    return dajax.json()
 
