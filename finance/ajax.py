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
from finance.models import VoucherRequest, PaymentRequest, AdvanceRequest, Vendor
from finance.forms import VoucherForm, PaymentForm, AdvanceForm

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
    


#__________-- ADD VOUCHER FUNCTION--___________
"""
Accepts a serializedform and a Vendor ID, and creates and saves a voucher request
"""    
@dajaxice_register(method="GET", name="finance.newvoucher_get")
@dajaxice_register(method="POST", name="finance.newvoucher_post")
@login_required
def add_voucher_request (request, serializedform=None, vendorid=None):
    dajax = Dajax()
    
    print ("called")
    
    if request.method == 'POST':
        if (serializedform != None) and (vendorid != None):
            form = VoucherForm(deserialize_form(serializedform))
        else:
    #DEBUGGING LINE - ELIMINATE & REFINE LATER
            print ("No form/vendor ID sent")
            dajax.alert ("No form/vendorID sent")
            return dajax.json()
        
        if form.is_valid():
            newVoucher = form.save(commit=False)
            
            newVoucher.creator = request.user.get_profile()
            newVoucher.vendor = Vendor.objects.get(pk=vendorid)
            newVoucher.status = 'P'
            
            newVoucher.dept = request.user.get_profile().dept
            if request.user.get_profile().subdept:
                newVoucher.subdept = request.user.get_profile().subdept
     
            newVoucher.save()
            
            dajax.alert("Voucher Request successfully created")
            dajax.add_css_class('#id_modal', 'hide') # Hide modal
        else:
            dajax.remove_css_class('#form input', 'error')
            for error in form.errors:
                dajax.add_css_class('#id_%s' % error, 'error')   
    
    elif request.method == 'GET':
        if vendorid != None:
            form = VoucherForm()
            context = {'form': form, 'vendorid': vendorid, 'requesttype': "voucher", 'title': "New Voucher Request"}
            html_content = render_to_string('finance/form.html', context, context_instance=RequestContext(request))
            dajax.remove_css_class('#id_modal', 'hide') # Show modal
            dajax.assign("#id_modal", "innerHTML", html_content) # Populate modal
        else:
            dajax.alert ("No Vendor specified")
            
        
        
    return dajax.json()
    


#__________-- ADD PAYMENT FUNCTION--___________
"""
Accepts a serializedform, and creates and saves a payment request
"""      
@dajaxice_register(method="GET", name="finance.newpayment_get")
@dajaxice_register(method="POST", name="finance.newpayment_post")
@login_required
def add_payment_request (request, serializedform=None):
    dajax = Dajax()
    
    if request.method == 'POST':
        if (serializedform != None):
            form = PaymentForm(deserialize_form(serializedform))
        else:
#DEBUGGING LINE - ELIMINATE & REFINE LATER
            print ("No form sent")
            return dajax.json()
        
        if form.is_valid():
            newPayment = form.save(commit=False)
            
            newPayment.creator = request.user.get_profile()
            newPayment.status = 'P'
            
            newPayment.dept = request.user.get_profile().dept
            if request.user.get_profile().subdept:
                newPayment.subdept = request.user.get_profile().subdept
     
            newPayment.save()
            
            dajax.alert("Payment Request successfully created")
            dajax.add_css_class('#id_modal', 'hide') # Hide modal
        else:
            dajax.remove_css_class('#requestform input', 'error')
            for error in form.errors:
                dajax.add_css_class('#id_%s' % error, 'error')    
    
    elif request.method == 'GET':
        form = PaymentForm()
        context = {'form': form, 'requesttype': "payment", 'title': "New Payment Request"}
        html_content = render_to_string('finance/form.html', context, context_instance=RequestContext(request))
        dajax.remove_css_class('#id_modal', 'hide') # Show modal
        dajax.assign("#id_modal", "innerHTML", html_content) # Populate modal
        
    return dajax.json()
    



#__________-- ADD ADVANCE FUNCTION--___________
"""
Accepts a serializedform, and creates and saves an advance request
"""      
@dajaxice_register(method="GET", name="finance.newadvance_get")
@dajaxice_register(method="POST", name="finance.newadvance_post")
@login_required
def add_advance_request (request, serializedform=None):
    dajax = Dajax()
    
    if request.method == 'POST':
        if (serializedform != None):
            form = AdvanceForm(deserialize_form(serializedform))
        else:
    #DEBUGGING LINE - ELIMINATE & REFINE LATER
            print ("No form sent")
            return dajax.json()
        
        if form.is_valid():
            newAdvance = form.save(commit=False)
            
            newAdvance.creator = request.user.get_profile()
            newAdvance.status = 'P'
            
            newAdvance.dept = request.user.get_profile().dept
            if request.user.get_profile().subdept:
                newAdvance.subdept = request.user.get_profile().subdept
     
            newAdvance.save()
            
            dajax.alert("Advance Request successfully created")
            dajax.add_css_class('#id_modal', 'hide') # Hide modal
        else:
            dajax.remove_css_class('#requestform input', 'error')
            for error in form.errors:
                dajax.add_css_class('#id_%s' % error, 'error')
            
            
    elif request.method == 'GET':
        form = AdvanceForm()
        context = {'form': form, 'requesttype': "advance", 'title': "New Advance Request"}
        html_content = render_to_string('finance/form.html', context, context_instance=RequestContext(request))
        dajax.remove_css_class('#id_modal', 'hide') # Show modal
        dajax.assign("#id_modal", "innerHTML", html_content) # Populate modal
        
    return dajax.json()
