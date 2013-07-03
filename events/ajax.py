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
# From forms
from events.forms import EventDetailsForm, get_json_file_path
# From models
from users.models import ERPUser
from events.models import GenericEvent
# From Misc to show bootstrap alert
from misc.utilities import show_alert
# From ERP
from erp.settings import MEDIA_ROOT
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
        return json.dumps(return_dict, sort_keys=True, indent=4)
    with open(event_json_filepath) as f:
        return_dict = json.load(f) # This is a python object: has to be converted to a json object1
        f.close()
    return json.dumps(return_dict, sort_keys=False, indent=4)


@dajaxice_register(method="GET", name="events.edit_event_get")
@dajaxice_register(method="POST", name="events.edit_event_post")
# __________--- Send events edit page from json file ---___________#
def edit_event(request, event_name, edit_form=None):
    """
        This function renders the "edit event" page for Event coords
        args : event_name : The name of the event which needs to be edited
    """
    dajax = Dajax()
    html_content = ""
    event_query = GenericEvent.objects.filter(title=event_name)
    if event_query:
        event_instance = event_query[0]
    if request.method == 'POST' and edit_form != None:
        if event_query:
            form = EventDetailsForm(deserialize_form(edit_form), instance=event_instance)
        else:
            form = EventDetailsForm(deserialize_form(edit_form))
        if form.is_valid():
            form.save()
            dajax.script("alert('Form saved');")
        else:
            form = EventDetailsForm()
            dajax.script("alert('Form error');")
            html_content = render_to_string('events/edit.html', locals(), RequestContext(request))
    else:
        form = EventDetailsForm()
        html_content = render_to_string('events/edit.html', locals(), RequestContext(request))
    if html_content :
        dajax.assign("#id_content", "innerHTML", html_content) # Populate content
    
    return dajax.json()

