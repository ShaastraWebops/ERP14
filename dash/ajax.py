# For simple dajax(ice) functionalities
from django.utils import simplejson
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax

# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string

# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test

# From models
from tasks.models import Task, Comment, TASK_STATUSES
from users.models import ERPUser

# From Misc to show bootstrap alert
from misc.utilities import show_alert

# _____________--- TABLE OF CONTACTS ---______________#
@dajaxice_register(name="dash.contacts")
@login_required
def contacts(request):
    """
        Used to show table of all members participating in shaastra
        It creates a table for this.
        
        Renders in : right_content
        Refreshes : null
        
        EVERYONE :
            It can be seen by anyone who has signed in
            
        QUERIES TO RETRIEVE:
            1.  Every user's:
                > Name
                > Department
                > Designation
                > Contact
                > Link to profile
    """
    dajax = Dajax() # To hold the json
    
    userprofile = request.user.get_profile()
# Query dictionary will contain UserProfile and the table to be drawn
    query_dictionary = {} # Initialize a blank Query dictionary.
    query_dictionary["userprofile"] = userprofile
    query_dictionary["TASK_STATUSES"] = TASK_STATUSES # To search for status msg
    html_content = ""
    
    # ALL QUERYSETS OF TASKS FILTERED FOR THE USER MUST BE AGAIN FILTERED BY DEPARTMENT (the way I've done it for user_tasks). THIS HANDLES THE MULTIPLE IDENTITY DISORDER.
    # Assigning the above values
    # ALL
    all_users = ERPUser.objects.all()
    query_dictionary["users_info"] = []
    for u in all_users:
        user_info = { 
                        'iden' : u.id,
                        'name' : u.user.first_name + " " + u.user.last_name,
                        'dept' : u.get_dept_subdept(),
                        'desig' : u.get_position(),
                        'ph_mad' : u.chennai_number,
                        'ph_home' : u.summer_number,
                        'email' : u.user.email
                    }
        query_dictionary['users_info'].append(user_info)
    html_content = render_to_string("dash/contacts.html", query_dictionary, RequestContext(request))
        
    if html_content != "": 
        # put html generated above into json if not null
        # if null, alert has already been taken care of
        dajax.assign('#id_content_right','innerHTML', html_content)
    
    
    
    return dajax.json()
