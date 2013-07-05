# coding: utf-8

# ************** ERP - DASH APP - VIEWS ********************* #


from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from misc.dajaxice.core import dajaxice_functions

from tasks.models import Task



# _____________--- DASH VIEW ---______________#
"""
QUERIES TO RETRIEVE:
1.  The user’s tasks.
2.  Tasks assigned to the department
3.  Tasks assigned to the subdepartment
4.  The Crosstasks created by the department
5.  Tasks pending approval
6.  ?Crosstasks _to_ the department?


"""
@login_required
def dash_view(request):
    userprofile = request.user.get_profile()

    # Initialize a blank Query dictionary.
    query_dictionary = {}
    
    #passing the userprofile
    query_dictionary["userprofile"] = userprofile
    
    
    #RENDERING THE TEMPLATE
    # For a Coordinator
    if userprofile.status == 0:
        return render_to_response ('dash/coord.html', query_dictionary, context_instance=RequestContext(request))
        
    # For a Supercoordinator
    if userprofile.status == 1:
        return render_to_response ('dash/supercoord.html', query_dictionary, context_instance=RequestContext(request))
        
    # For a Core
    if userprofile.status == 2:
        return render_to_response ('dash/core.html', query_dictionary, context_instance=RequestContext(request))
        
        
