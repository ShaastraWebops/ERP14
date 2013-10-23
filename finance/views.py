from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from misc.dajaxice.core import dajaxice_functions
from finance.models import Vendor, BudgetProposal
import datetime

#Importing Model Formset Factory
from django.forms.models import modelform_factory

#Import Django Exception
from django.core.exceptions import ObjectDoesNotExist

##FOR TESTING
from django.http import HttpResponse


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


