# For simple dajax(ice) functionalities
from django.utils import simplejson
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
from misc.dajaxice.utils import deserialize_form
# Django imports
# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string
# Decorators
from django.contrib.auth.decorators import login_required
# For converting model to a dictionary that can be input into a ModelForm
from django.forms.models import model_to_dict
# From forms
from events.forms import EventDetailsForm, TabDetailsForm, get_json_file_path
# From models
from users.models import ERPUser
from events.models import GenericEvent, Tab
# From Misc to show bootstrap alert
from misc.utilities import show_alert
# From ERP
from erp.settings import MEDIA_ROOT
from erp.variables import events_being_edited
# Python imports
import json
import os

@dajaxice_register
def hello_world(request):
    """
        Used for testing Dajax + Dajaxice
    """
    dajax = Dajax()
    dajax.assign('#id_content','innerHTML', "Hello world !")
    #dajax.alert("Hello World!")
    return dajax.json()
    
@dajaxice_register
def hello(request):
    """
        Used for testing Dajaxice
    """
    #html_content = render_to_string("dash/task_tables/coord_you.html", query_dictionary, RequestContext(request))
    return simplejson.dumps({'message': 'hello'})

@dajaxice_register
# __________--- Send events data from json file ---___________#
def get_event(request, event_name):
    """
        This function gets the data from the json file and gives it to dajaxice
        The processing of the json happens at the client side
        Note : Does NOT use Dajax. The json data needs to be parsed separately.
    """
    return_dict = {}
    event_json_filepath = get_json_file_path(event_name + '.json')
    if not os.path.exists(event_json_filepath): # No file found, give error message
        return_dict['id_alert'] = {'type' : 'error', 'msg' : 'No event found'}
        return json.dumps(return_dict, sort_keys=False, indent=4)
    with open(event_json_filepath) as f:
        return_dict = json.load(f) # This is a python object: has to be converted to a json object1
        f.close()
    return json.dumps(return_dict, sort_keys=False, indent=4)

@dajaxice_register
# __________--- Send events data from json file ---___________#
def show_event_erp(request, event_name=None, event_pk=None):
    """
        This function gets the data from the json file and gives it to 
        the template to show it in nice html content. This template is for ERP.
        Mainsite may require another template.
        
        You can query based on name or pk.
    """
    dajax = Dajax()
    json_dict = {}
    event_instance = None
    
    # Argument validation
    if not ( event_name or event_pk ): # Neither arg given
        show_alert(dajax, "error", "There is some error on the site, please report to WebOps team")
        return dajax.json()
    elif event_name and event_pk: # Both args given ..
        show_alert(dajax, "error", "There is some error on the site, please report to WebOps team.")
        return dajax.json()
    elif event_pk:
        event_query = GenericEvent.objects.filter(pk=event_pk)
    elif event_name:
        event_query = GenericEvent.objects.filter(title=event_name)
    
    if event_query:
        event_instance = event_query[0]
        event_pk = event_instance.pk
        tab_list = Tab.objects.filter(event=event_instance) # for providing the list of tabs to erp_tabs.html
    else:
        show_alert(dajax, "error", "This event has not been created on the site. Contact WebOps team.")
        return dajax.json()
    
    event_json_filepath = get_json_file_path(str(event_pk) + '_' + event_name + '.json')
    print event_json_filepath
    
    if not os.path.exists(event_json_filepath): # No file found
        # if the event exists in db but no json file present, then create a json file with the event and its tabs' details
        if event_instance:
            event_dict = model_to_dict(event_instance)
            form = EventDetailsForm(event_dict, instance=event_instance)
            if form.is_valid():
                form.save()
            for tab in tab_list:
                tab_dict = model_to_dict(tab)
                print tab_dict
                tab_form = TabDetailsForm(tab_dict, instance=tab)
                if tab_form.is_valid():
                    tab_form.save()
        else: # return an empty page and let the user add event details
            show_alert(dajax, "error", "Event details not found. Click Edit Event Details button to add details to this event.")
            html_content = render_to_string('events/erp_tabs.html', locals(), RequestContext(request))
            dajax.assign("#id_content_right", "innerHTML", html_content)
            return dajax.json()
    with open(event_json_filepath) as f:
        json_dict = json.dumps(json.load(f), sort_keys=False, indent=4) # This is a json object
        html_content = render_to_string('events/erp_tabs.html', locals(), RequestContext(request))
        f.close()
    
    # Now that json data is in json_dict : populate in a template and give
    if html_content:
        dajax.assign("#id_content_right", "innerHTML", html_content) # Populate content
        #dajax.script("display_event_erp($('#json_dict_content').val());") # run the function to populate the json content
        
    return dajax.json()

@dajaxice_register(method="GET", name="events.edit_event_get")
@dajaxice_register(method="POST", name="events.edit_event_post")
# __________--- Send events edit page from json file ---___________#
def edit_event(request, event_name=None, event_pk=None, edit_form=None):
    """
        This function renders the "edit event" page for Event coords
        args : 
            event_name - The name of the event which needs to be edited
            event_pk - The pk of the event which needs to be edited
            edit_Form - The edited form in post requests
        
        Check before savin
            - check if event in erp.variables.event_being_edited
            - check if name changed, if yes : change file name
    """
    dajax = Dajax()
    html_content = ""
    event_query = None
    event_instance = None
    
    # Argument validation
    if not ( event_name or event_pk ): # Neither arg given
        show_alert(dajax, "error", "There is some error on the site, please report to WebOps team")
        return dajax.json()
    elif event_name and event_pk: # Both args given ..
        show_alert(dajax, "error", "There is some error on the site, please report to WebOps team.")
        return dajax.json()
    elif event_pk:
        event_query = GenericEvent.objects.filter(pk=event_pk)
    elif event_name:
        event_query = GenericEvent.objects.filter(title=event_name)

    if event_query: # get event details and tab details
        event_instance = event_query[0]
    else:
        show_alert(dajax, "error", "This event does not exist on the site, please report to WebOps team.")
        return dajax.json()
    
    # Now, event_instance has the instance of the event passed to this function.
    # Use it. Nothing else from the top is connected here.
    if request.method == 'POST' and edit_form != None:
        form = EventDetailsForm(deserialize_form(edit_form), instance = event_instance)
        if event_instance.title in events_being_edited:
            show_alert(dajax, "error", "This event was just updated by another user. Your changes will over write previous changes")
        elif form.is_valid(): # Save form and json
            clean_form = form.clean()
            
            # Handles the form and sql
            form.save()
            
            # Handles the json :
            json_dict = {}
            # Add to global list for file concurrency issue - so no one can open file while it is being used
            events_being_edited.append(event_instance.pk)
            # Check if file title has changed
            event_name_new = clean_form['title']
            event_name_old = event_instance.title
            event_pk = event_instance.pk
            event_json_filepath_new = get_json_file_path(str(event_pk) + '_'+ event_name_new + '.json')
            if event_name_new != event_name_old: # Rename the json file ! the names are different
                event_json_filepath_old = get_json_file_path(str(event_pk) + '_'+ event_name_old + '.json')
                os.rename(event_json_filepath_old, event_json_filepath_new)
            with open(event_json_filepath_new) as f:
                json_dict = json.dumps(json.load(f), sort_keys=False, indent=4) # This is a json object
                html_content = render_to_string('events/edit_event.html', locals(), RequestContext(request))
                f.close()
            dajax.remove_css_class('#id_form input', 'error')
            show_alert(dajax, "success", "Event edited successfully")
        else:
            error_string = "<br />"
            dajax.remove_css_class('#id_form input', 'error')
            for error in form.errors:
                error_string += error[0].upper() + error[1:] + ": " + form.errors[error][0] + "<br />"
                dajax.add_css_class('#id_%s' % error, 'error')

            form = EventDetailsForm()
            show_alert(dajax, "error", error_string)
            html_content = render_to_string('events/edit_event.html', locals(), RequestContext(request)) # show edit form again
    else:
        form = EventDetailsForm(instance = event_instance)
        html_content = render_to_string('events/edit_event.html', locals(), RequestContext(request))

    if html_content :
        dajax.assign("#event_" + str(event_instance.pk), "innerHTML", html_content) # Populate content

    return dajax.json()

@dajaxice_register(method="GET", name="events.new_tab_get")
@dajaxice_register(method="POST", name="events.new_tab_post")
# __________--- Send events edit page from json file ---___________#
def new_tab(request, tab_pk=None, form=None):
    """
        This function renders the "edit event" page for Event coords
        args :
            tab_pk - the pk of the tab being edited
            form - the form sent in post request
            
        Check before savin
            - check if event in erp.variables.event_being_edited
            - check if name changed, if yes : change file name
    """
    dajax = Dajax()
    html_content = ""
    if tab.pk:
        tab_instance = Tab.objects.get(pk=tab_pk)
    else:
        tab_instance = None
    
    if request.method == 'POST' and edit_form != None:
        form = EventDetailsForm(deserialize_form(edit_form), instance = event_instance)
        if event_instance.title in events_being_edited:
            show_alert(dajax, "error", "This event was just updated by another user. Your changes will over write previous changes")
        elif form.is_valid(): # Save form and json
            clean_form = form.clean()
            
            # Handles the form and sql
            form.save()
            
            # Handles the json :
            json_dict = {}
            # Add to global list for file concurrency issue - so no one can open file while it is being used
            events_being_edited.append(event_instance.pk)
            # Check if file title has changed
            event_name_new = clean_form['title']
            event_name_old = event_instance.title
            event_pk = event_instance.pk
            event_json_filepath_new = get_json_file_path(str(event_pk) + '_'+ event_name_new + '.json')
            if event_name_new != event_name_old: # Rename the json file ! the names are different
                event_json_filepath_old = get_json_file_path(str(event_pk) + '_'+ event_name_old + '.json')
                os.rename(event_json_filepath_old, event_json_filepath_new)
            with open(event_json_filepath_new) as f:
                json_dict = json.dumps(json.load(f), sort_keys=False, indent=4) # This is a json object
                html_content = render_to_string('events/edit_event.html', locals(), RequestContext(request))
                f.close()
            dajax.remove_css_class('#id_form input', 'error')
            show_alert(dajax, "success", "Event edited successfully")
        else:
            error_string = "<br />"
            dajax.remove_css_class('#id_form input', 'error')
            for error in form.errors:
                error_string += error[0].upper() + error[1:] + ": " + form.errors[error][0] + "<br />"
                dajax.add_css_class('#id_%s' % error, 'error')

            form = EventDetailsForm()
            show_alert(dajax, "error", error_string)
            html_content = render_to_string('events/edit_tab.html', locals(), RequestContext(request)) # show edit form again
    else:
        if tab_instance:
            form = TabDetailsForm(instance = tab_instance)
        else:
            form = TabDetailsForm()
        html_content = render_to_string('events/edit_tab.html', locals(), RequestContext(request))

    if html_content :
        dajax.assign("#event_" + str(event_instance.pk), "innerHTML", html_content) # Populate content

    return dajax.json()
