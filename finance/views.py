from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from misc.dajaxice.core import dajaxice_functions
import datetime

#Importing Model Formset Factory
from django.forms.models import modelform_factory

#Import Django Exception
from django.core.exceptions import ObjectDoesNotExist

from finance.models import Vendor, BudgetProposal
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
@login_required
def create_budget(request):
    BudgetForm = modelform_factory(BudgetProposal, fields=('comment', 'plan_1_total', 'plan_2_total', 'plan_1_description', 'plan_2_description') )
    
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            newbudget = form.save(commit=False)
            
            newbudget.creator = request.user.get_profile()
            newbudget.event = request.user.get_profile().event
            
            newbudget.save()
            
            return redirect('finance.views.home')
        else:
            return render_to_response ('finance/createbudget.html', {'form': form }, context_instance=RequestContext(request))
    else:
        #Display Blank Form
        form = BudgetForm()
        context = {'form': form}
        return render_to_response('finance/createbudget.html', context, context_instance=RequestContext(request))
        

@login_required
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
        
        return redirect('finance.views.home')
    except ObjectDoesNotExist:
        return redirect('finance.views.home')
        
        
@login_required
def finance_budget_portal(request):
    #Passing a context of information to the template
    context = {}
    
    #Userprofile
    context["userprofile"] = request.user.get_profile()
    
    #Unapproved Budgets
    context["unapproved"] = BudgetProposal.objects.filter(isapproved=False)
    
    #Approved Budgets
    context["approved"] = BudgetProposal.objects.filter(isapproved=True)
    
    return render_to_response('finance/financebudgetportal.html', context, context_instance=RequestContext(request))
    


@login_required
def budget_page(request, primkey):
    try:
        approvedbudget = BudgetProposal.objects.get(pk=primkey)
        
        context = {}
        context["budget"] = approvedbudget
        
        return render_to_response('finance/budgetpage.html', context, context_instance=RequestContext(request))
    except ObjectDoesNotExist:
        return redirect('finance.views.home')



#######################################----------VOUCHERS VIEWS----------###############################################


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






@login_required
def user_voucher_history(request, curr_vendor):
    """
        Used to display a user's history with a particular vendor
        """
    
    userprofile = request.user.get_profile()
    query_dictionary = {}
    query_dictionary['approved_vouchers'] = VoucherRequest.objects.filter(creator=userprofile).all()
    #    query_dictionary['pending_vouchers'] = VoucherRequest.objects.filter(creator=userprofile).filter(vendor.name=curr_vendor).filter(status='P').all()
    return render_to_response ('finance/voucher_history.html', query_dictionary, context_instance = RequestContext(request) )
    
    
    
    
    
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
            
            return redirect('finance.views.home')
        else:
            context = {'form': form, 'vendorid': vendorid, 'title': "New Voucher Request"}
            return render_to_response ('finance/form.html', context, context_instance=RequestContext(request))   
    
    else:
        form = VoucherForm()
        context = {'form': form, 'vendorid': vendorid, 'title': "New Voucher Request"}
        return render_to_response ('finance/form.html', context, context_instance=RequestContext(request))



#######################################----------PAYMENTS VIEWS----------###############################################



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
            
            return redirect('finance.views.home')
        else:
            context = {'form': form, 'title': "New Payment Request"}
            return render_to_response ('finance/form.html', context, context_instance=RequestContext(request))    
    
    elif request.method == 'GET':
        form = PaymentForm()
        context = {'form': form, 'title': "New Payment Request"}
        return render_to_response ('finance/form.html', context, context_instance=RequestContext(request))
        
        
        
        
        
#######################################----------ADVANCES VIEWS----------###############################################






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
            
            return redirect('finance.views.home')
        else:
            context = {'form': form, 'title': "New Advance Request"}
            return render_to_response ('finance/form.html', context, context_instance=RequestContext(request)) 
    
    
    else:
        form = AdvanceForm()
        context = {'form': form, 'title': "New Advance Request"}
        return render_to_response ('finance/form.html', context, context_instance=RequestContext(request)) 
