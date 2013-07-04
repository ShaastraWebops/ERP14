# coding: utf-8

# ************** ERP - DASH APP - VIEWS ********************* #


from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from misc.dajaxice.core import dajaxice_functions

from tasks.models import Task
from users.models import ERPUser


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
    
    #ALL QUERYSETS OF TASKS FILTERED FOR THE USER MUST BE AGAIN FILTERED BY DEPARTMENT (the way I've done it for user_tasks). THIS HANDLES THE MULTIPLE IDENTITY DISORDER.
    #Assigning the above values
    query_dictionary["user_tasks"] = userprofile.task_set.filter(targetdept=userprofile.dept).all()
    
    #COORD ONLY
    #The attribute userprofile.subdept is present only if he's a coord
    if userprofile.status == 0:
        query_dictionary["subdept_tasks"] = userprofile.subdept.task_set.exclude(taskstatus='U')
    
    #CORE & SUPERCOORD
    if ((userprofile.status == 1) or (userprofile.status == 2)):
        query_dictionary["dept_todo_crosstasks"] = userprofile.dept.todo_task_set.filter(isxdepartmental=True).exclude(taskstatus='U') #Remove if necessary.
        query_dictionary["dept_tasks"] = userprofile.dept.todo_task_set.exclude(taskstatus='U')
    
    #CORE ONLY
    if userprofile.status == 2:
        query_dictionary["dept_created_crosstasks"] = userprofile.dept.created_task_set.filter(isxdepartmental=True)
        query_dictionary["approval_pending_tasks"] = userprofile.dept.todo_task_set.filter(taskstatus='U')
    
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
        
        
