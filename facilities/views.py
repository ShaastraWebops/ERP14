# Create your views here.
# Create your views here.
# Imports
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
import datetime

#Import Add Facility Item form
from facilities.forms import FacilityItemForm

#Import Utilities
from misc.utilities import events_core_check, events_coord_check, events_check

#Importing necessary models
from facilities.models import FacilityOrder, ItemEntry, FacilityItem

#Importing Model Formset Factory
from django.forms.models import modelformset_factory

#Import Django Exception
from django.core.exceptions import ObjectDoesNotExist



#_______________________---ADD MENU ITEM---_________________________
@login_required
@user_passes_test(events_core_check)
def AddMenuItem(request):
    if request.method == 'POST':
        form = FacilityItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facilities.views.FacilitiesHome')
        else:
            return render_to_response ('facilities/additemtomenu.htm', {'form': form }, context_instance=RequestContext(request))
    else:
        #Display Blank Form
        form = FacilityItemForm()
        context = {'form': form}
        return render_to_response('facilities/additemtomenu.htm', context, context_instance=RequestContext(request))



#___________________________---CREATE ORDER VIEW---___________________________
"""
    PRESENTS AND PROCESSES ORDER FORMSETS
    Presents a formset to a user. This is the user's order. The user then adds entries to his order,
    and submits the form.
    
    The submitted form is processed by the same view. It handles repetition of items, and adds entries
    to the order appropriately.
    """
@login_required
@user_passes_test(events_check)
def CreateOrder(request):
    #Create a formset for various entries in the creator's order.
    OrderFormset = modelformset_factory(ItemEntry, fields=('facilityitem', 'quantity', 'description'), max_num=1, extra=1)
    
    #For a POST request: Process the data/Add a new row.
    #Code to add a row
    if request.method=='POST':
        if 'add' in request.POST:
            postdata = request.POST.copy()
            postdata['ord-TOTAL_FORMS'] = int(postdata['ord-TOTAL_FORMS']) + 1
            formset = OrderFormset(postdata, prefix='ord')
            showerrors = False
            return render_to_response('facilities/createorder.htm', {'formset': formset, 'showerrors': showerrors}, context_instance=RequestContext(request))
        if 'remove' in request.POST:
            postdata = request.POST.copy()
            postdata['ord-TOTAL_FORMS'] = int(postdata['ord-TOTAL_FORMS']) - 1
            formset = OrderFormset(postdata, prefix='ord')
            showerrors = False
            return render_to_response('facilities/createorder.htm', {'formset': formset, 'showerrors': showerrors}, context_instance=RequestContext(request))
        #Code to process data
        elif 'submit' in request.POST:
            formset = OrderFormset(request.POST, request.FILES, queryset=ItemEntry.objects.none(), prefix = 'ord')
            if formset.is_valid() and formset.has_changed():
                #If the user has entered data, and if it's valid then:
                
                #Register a new order
                neworder = FacilityOrder(creator=request.user.get_profile())
                neworder.save()
                
                #Individually process entries in the order
                entries = formset.save(commit=False)
                
                for itementryinstance in entries:
                    """
                        Note:
                        Adding separate entries for identical facility items is ALLOWED currently.
                        This is because the separate entries might be listed for different purposes,
                        which can be elaborated on using the Description Field.
                    """
                    itementryinstance.order = neworder
                    itementryinstance.save()
                
                return redirect('facilities.views.FacilitiesHome')
            else:
                #Return the form with its errors.
                showerrors = True
                return render_to_response('facilities/createorder.htm', {'formset': formset, 'showerrors': showerrors}, context_instance=RequestContext(request))
    
    else:
        formset = OrderFormset(queryset=ItemEntry.objects.none(), prefix='ord')
        return render_to_response('facilities/createorder.htm', {'formset': formset}, context_instance=RequestContext(request))



#______________________---FACILITIES HOME---_____________________
@login_required
@user_passes_test(events_check)
def FacilitiesHome(request):
    userprofile = request.user.get_profile()

    #Passing a context of information to the template
    context = {}
    
    #Userprofile
    context["userprofile"] = userprofile
    
    context["isapprover"] = events_core_check(request.user)
    
    #Facility Items:
    context["facilityitems"] = FacilityItem.objects.all()
    
    #Pending & approved orders:
    if events_core_check(request.user):
        context["pending"] = FacilityOrder.objects.filter(isapproved=False)
        context["approved"] = FacilityOrder.objects.filter(isapproved=True)
    else:
        context["pending"] = userprofile.facilityorder_created_set.filter(isapproved=False)
        context["approved"] = userprofile.facilityorder_created_set.filter(isapproved=True)    
    
    return render_to_response('facilities/ordersummary.htm', context, context_instance=RequestContext(request))



#______________________---CLEAR AN ORDER---_____________________

@login_required
@user_passes_test(events_core_check)
def ApproveOrder(request, primkey):
    try:
        approvedorder = FacilityOrder.objects.get(pk=primkey)
        approvedorder.isapproved = True
        approvedorder.dateapproved = datetime.datetime.now()
        approvedorder.approver = request.user.get_profile()
        approvedorder.save()
        return redirect('facilities.views.FacilitiesHome')
    except ObjectDoesNotExist:
        return redirect('facilities.views.FacilitiesHome')
        
        
#______________________---Redirector---_____________________
@login_required
def FacilitiesRedirect(request):
    return redirect('facilities.views.FacilitiesHome')