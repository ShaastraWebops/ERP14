from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from misc.dajaxice.core import dajaxice_functions
import datetime

#Importing Decorators
from misc.utilities import finance_check, events_check, finance_or_events_check

#Importing Model Formset Factory
from django.forms.models import modelform_factory

#Import Django Exception
from django.core.exceptions import ObjectDoesNotExist

from finance.models import Vendor, BudgetProposal, VoucherRequest, PaymentRequest, AdvanceRequest
from finance.forms import PaymentForm, VoucherForm, AdvanceForm

##FOR TESTING
from django.http import HttpResponse





@login_required
def home ( request ) :
    
    userprofile = request.user.get_profile()
    
    query_dictionary = {}
    query_dictionary['userprofile'] = userprofile
    
    return render_to_response ( 'finance/home.html', query_dictionary, context_instance = RequestContext ( request ) )
    
    
    

#######################################----------BUDGETING VIEWS----------###############################################


#__________-- CREATE BUDGET --___________        
@login_required
@user_passes_test (events_check)
def create_budget(request):
    BudgetForm = modelform_factory(BudgetProposal, fields=('comment', 'plan_1_total', 'plan_2_total', 'plan_1_description', 'plan_2_description') )
    
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            newbudget = form.save(commit=False)
            
            newbudget.creator = request.user.get_profile()
            newbudget.event = request.user.get_profile().event
            
            newbudget.save()
            
            return redirect('finance.views.budgeting')
        else:
            user_dept = str(request.user.get_profile().dept)
            return render_to_response ('finance/createbudget.html', {'form': form, 'user_dept': user_dept}, context_instance=RequestContext(request))
    else:
        #Display Blank Form
        form = BudgetForm()
        user_dept = str(request.user.get_profile().dept)
        context = {'form': form, 'user_dept':user_dept}
        return render_to_response('finance/createbudget.html', context, context_instance=RequestContext(request))
        





#__________-- APPROVE BUDGET --___________        
@login_required
@user_passes_test (finance_check)
def approve_budget(request, primkey, option):
    try:
        approvedbudget = BudgetProposal.objects.get(pk=primkey)
        
        #Validate
        if (approvedbudget.isapproved == True) or (int(option) > 2) or (int(option) < 1):
            return redirect('finance.views.home')
        
        approvedbudget.isapproved = True
        approvedbudget.dateapproved = datetime.datetime.now()
        approvedbudget.approver = request.user.get_profile()
        approvedbudget.selectedplan = option
        approvedbudget.save()
        
        return redirect('finance.views.budgeting')
    except ObjectDoesNotExist:
        return redirect('finance.views.budgeting')
        




#__________-- BUDGETING HOME --___________        
@login_required
@user_passes_test (finance_or_events_check)
def budgeting(request):
    #Passing a context of information to the template
    context = {}
    
    #Userprofile
    userprofile = request.user.get_profile()
    context["userprofile"] = userprofile
    context["isevents"] = userprofile.dept.name == 'Events'
    
    if ( context["userprofile"].dept.name == 'Finance' ):
        #Unapproved Budgets
        context["unapproved"] = BudgetProposal.objects.filter(isapproved=False)
        
        #Approved Budgets
        context["approved"] = BudgetProposal.objects.filter(isapproved=True)
    else:
        #Unapproved Budgets
        context["unapproved"] = BudgetProposal.objects.filter(isapproved=False).filter(creator=userprofile)
        
        #Approved Budgets
        context["approved"] = BudgetProposal.objects.filter(isapproved=True).filter(creator=userprofile)
    
    return render_to_response('finance/budgeting.html', context, context_instance=RequestContext(request))
    





#__________-- VIEW A BUDGET --___________        
@login_required
@user_passes_test (finance_or_events_check)
def budget_page(request, primkey):
    try:
        approvedbudget = BudgetProposal.objects.get(pk=primkey)
        
        context = {}
        context["budget"] = approvedbudget
        context["user_dept"] = str(request.user.get_profile().dept)
        
        return render_to_response('finance/budgetpage.html', context, context_instance=RequestContext(request))
    except ObjectDoesNotExist:
        return redirect('finance.views.budgeting')



#######################################----------VOUCHERS VIEWS----------###############################################

"""
TODO:
    UNIQUE ID IMPLEMENTATION
"""

#__________-- VOUCHERS HOME --___________
@login_required
def vouchers (request, vendorid=None) :

    userprofile = request.user.get_profile()

    query_dictionary = {}
    query_dictionary['userprofile'] = userprofile
    query_dictionary['isfinance'] = ( userprofile.dept.name == 'Finance' )
    query_dictionary['vendors'] = Vendor.objects.all()
    
    if vendorid is not None:
        try:
            if query_dictionary['isfinance']:
                query_dictionary['vendor'] = Vendor.objects.get(pk=vendorid)
                query_dictionary['unapproved'] = VoucherRequest.objects.filter(vendor = query_dictionary['vendor']).filter(status='P').all()
                query_dictionary['approved'] = VoucherRequest.objects.filter(vendor = query_dictionary['vendor']).filter(status='A').all()
            else:
                query_dictionary['vendor'] = Vendor.objects.get(pk=vendorid)
                query_dictionary['unapproved'] = VoucherRequest.objects.filter(creator=userprofile).filter(vendor = query_dictionary['vendor']).filter(status='P').all()
                query_dictionary['approved'] = VoucherRequest.objects.filter(creator=userprofile).filter(vendor = query_dictionary['vendor']).filter(status='A').all()
        except ObjectDoesNotExist:
            query_dictionary['vendor'] = None
            query_dictionary['unapproved'] = None
            query_dictionary['approved'] = None


    #If the user is a finance coord
    #if query_dictionary['isfinance']:
	#return render_to_response ('finance/voucher_fin.html', query_dictionary, context_instance = RequestContext ( request ) )

    #If the user is a gen coord
    return render_to_response ( 'finance/vouchers.html', query_dictionary, context_instance = RequestContext ( request ) )
    
    


#__________-- VOUCHER PAGE --___________
@login_required
def voucher_page(request, primkey):
    try:
        voucher = VoucherRequest.objects.get(pk=primkey)
        
        context = {}
        context["isfinance"] = ( request.user.get_profile().dept.name == 'Finance' )
        context["voucher"] = voucher
        context["isapproved"] = (voucher.status == 'A')
        
        return render_to_response('finance/voucherpage.html', context, context_instance=RequestContext(request))
    except ObjectDoesNotExist:
        return redirect('finance.views.vouchers')







#__________-- APPROVE VOUCHER FUNCTION--___________
@login_required
@user_passes_test (finance_check)
def approve_voucher(request, primkey):
    try:
        approvedvoucher = VoucherRequest.objects.get(pk=primkey)
        
        #Validate
        if (approvedvoucher.status == 'A'):
            return redirect('finance.views.home')
        
        approvedvoucher.status = 'A'
        approvedvoucher.dateapproved = datetime.datetime.now()
        approvedvoucher.approver = request.user.get_profile()
        approvedvoucher.save()
        
        return redirect('finance.views.vouchers')
    except ObjectDoesNotExist:
        return redirect('finance.views.vouchers')
    
    
    
#__________-- ADD VOUCHER FUNCTION--___________
@login_required
def add_voucher_request (request, vendorid):
    if request.method == 'POST':
        form = VoucherForm(request.POST)
        
        if form.is_valid():
            newVoucher = form.save(commit=False)
            
            newVoucher.creator = request.user.get_profile()
            newVoucher.vendor = Vendor.objects.get(pk=vendorid)
            newVoucher.status = 'P'
            
            newVoucher.dept = request.user.get_profile().dept
            if request.user.get_profile().subdept:
                newVoucher.subdept = request.user.get_profile().subdept
            
            newVoucher.save()
            
            return redirect('finance.views.vouchers')
        else:
            context = {'form': form, 'vendorid': vendorid, 'title': "New Voucher Request"}
            return render_to_response ('finance/createvoucher.html', context, context_instance=RequestContext(request))   
    
    else:
        form = VoucherForm()
        context = {'form': form, 'vendorid': vendorid, 'title': "New Voucher Request"}
        return render_to_response ('finance/createvoucher.html', context, context_instance=RequestContext(request))



#######################################----------PAYMENTS VIEWS----------###############################################
"""
TODO:
    CHECK NUMBER IMPLEMENTATION
"""


#__________-- PAYMENTS HOME--___________
@login_required
def payments(request):
    #Passing a context of information to the template
    context = {}
    
    #Userprofile
    userprofile = request.user.get_profile()
    context["userprofile"] = userprofile
    context["isfinance"] = ( request.user.get_profile().dept.name == 'Finance' )
    
    if ( context["userprofile"].dept.name == 'Finance' ):
        #Unapproved Budgets
        context["unapproved"] = PaymentRequest.objects.filter(status = 'P')
        
        #Approved Budgets
        context["approved"] = PaymentRequest.objects.filter(status = 'A')
    else:
        #Unapproved Budgets
        context["unapproved"] = PaymentRequest.objects.filter(status = 'P').filter(creator=userprofile)
        
        #Approved Budgets
        context["approved"] = PaymentRequest.objects.filter(status = 'A').filter(creator=userprofile)
    
    return render_to_response('finance/payments.html', context, context_instance=RequestContext(request))
    
    
    
#__________-- PAYMENT PAGE --___________
@login_required
def payment_page(request, primkey):
    try:
        payment = PaymentRequest.objects.get(pk=primkey)
        
        context = {}
        context["isfinance"] = ( request.user.get_profile().dept.name == 'Finance' )
        context["payment"] = payment
        context["isapproved"] = (payment.status == 'A')
        
        return render_to_response('finance/paymentpage.html', context, context_instance=RequestContext(request))
    except ObjectDoesNotExist:
        return redirect('finance.views.payments')
    
    
    
    
#__________-- APPROVE PAYMENT FUNCTION--___________
@login_required
@user_passes_test (finance_check)
def approve_payment(request, primkey):
    try:
        approvedpayment = PaymentRequest.objects.get(pk=primkey)
        
        #Validate
        if (approvedpayment.status == 'A'):
            return redirect('finance.views.home')
        
        approvedpayment.status = 'A'
        approvedpayment.dateapproved = datetime.datetime.now()
        approvedpayment.approver = request.user.get_profile()
        approvedpayment.save()
        
        return redirect('finance.views.payments')
    except ObjectDoesNotExist:
        return redirect('finance.views.payments')
    



#__________-- ADD PAYMENT FUNCTION--___________
@login_required
def add_payment_request (request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        
        if form.is_valid():
            newPayment = form.save(commit=False)
            
            newPayment.creator = request.user.get_profile()
            newPayment.status = 'P'
            
            newPayment.dept = request.user.get_profile().dept
            if request.user.get_profile().subdept:
                newPayment.subdept = request.user.get_profile().subdept
            
            newPayment.save()
            
            return redirect('finance.views.payments')
        else:
            context = {'form': form, 'title': "New Payment Request"}
            return render_to_response ('finance/createpayment.html', context, context_instance=RequestContext(request))    
    
    elif request.method == 'GET':
        form = PaymentForm()
        context = {'form': form, 'title': "New Payment Request"}
        return render_to_response ('finance/createpayment.html', context, context_instance=RequestContext(request))
        
        
        
        
        
#######################################----------ADVANCES VIEWS----------###############################################



#__________-- ADVANCES HOME--___________
@login_required
def advances(request):
    #Passing a context of information to the template
    context = {}
    
    #Userprofile
    userprofile = request.user.get_profile()
    context["userprofile"] = userprofile
    context["isfinance"] = ( request.user.get_profile().dept.name == 'Finance' )
    
    if ( context["userprofile"].dept.name == 'Finance' ):
        #Unapproved Budgets
        context["unapproved"] = AdvanceRequest.objects.filter(status = 'P')
        
        #Approved Budgets
        context["approved"] = AdvanceRequest.objects.filter(status = 'A')
    else:
        #Unapproved Budgets
        context["unapproved"] = AdvanceRequest.objects.filter(status = 'P').filter(creator=userprofile)
        
        #Approved Budgets
        context["approved"] = AdvanceRequest.objects.filter(status = 'A').filter(creator=userprofile)
    
    return render_to_response('finance/advances.html', context, context_instance=RequestContext(request))
    
    


#__________-- ADVANCE PAGE --___________
@login_required
def advance_page(request, primkey):
    try:
        advance = AdvanceRequest.objects.get(pk=primkey)
        
        context = {}
        context["isfinance"] = ( request.user.get_profile().dept.name == 'Finance' )
        context["advance"] = advance
        context["isapproved"] = (advance.status == 'A')
        
        return render_to_response('finance/advancepage.html', context, context_instance=RequestContext(request))
    except ObjectDoesNotExist:
        return redirect('finance.views.advances')
    
    


#__________-- APPROVE ADVANCE FUNCTION--___________
@login_required
@user_passes_test (finance_check)
def approve_advance(request, primkey):
    try:
        approvedadvance = AdvanceRequest.objects.get(pk=primkey)
        
        #Validate
        if (approvedadvance.status == 'A'):
            return redirect('finance.views.advances')
        
        approvedadvance.status = 'A'
        approvedadvance.dateapproved = datetime.datetime.now()
        approvedadvance.approver = request.user.get_profile()
        approvedadvance.save()
        
        return redirect('finance.views.advances')
    except ObjectDoesNotExist:
        return redirect('finance.views.advances')



#__________-- ADD ADVANCE FUNCTION--___________
@login_required
def add_advance_request (request):
    if request.method == 'POST':
        form = AdvanceForm(request.POST)
        
        if form.is_valid():
            newAdvance = form.save(commit=False)
            
            newAdvance.creator = request.user.get_profile()
            newAdvance.status = 'P'
            
            newAdvance.dept = request.user.get_profile().dept
            if request.user.get_profile().subdept:
                newAdvance.subdept = request.user.get_profile().subdept
            
            newAdvance.save()
            
            return redirect('finance.views.advances')
        else:
            context = {'form': form, 'title': "New Advance Request"}
            return render_to_response ('finance/createadvance.html', context, context_instance=RequestContext(request)) 
    
    
    else:
        form = AdvanceForm()
        context = {'form': form, 'title': "New Advance Request"}
        return render_to_response ('finance/createadvance.html', context, context_instance=RequestContext(request)) 
