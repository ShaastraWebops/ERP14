from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from events.forms import EventDetailsForm,UpdateForm,UploadTabFiles

from misc.dajaxice.core import dajaxice_functions

import os
from erp.settings import MEDIA_ROOT

import json

# __________--- Get place to store JSON - for events ---___________#
def get_json_file_path(filename):
    file_path = os.path.abspath( os.path.join( MEDIA_ROOT, 'json', 'events') )
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return os.path.join(file_path, filename)

# __________--- Show a json file on screen ---___________#
def home(request):
    event_json_filepath = get_json_file_path('test.json')
    if not os.path.exists(event_json_filepath):
        message = 'No event details to display.'
        return render_to_response('events/home.html', {'message': message})
    with open(event_json_filepath) as f:
        event_details = json.load(f) # This is a python object: has to be converted to a json object1
        f.close()
    event_details = json.dumps(event_details, sort_keys=True, indent=4) # This gives a json object
    return render_to_response('events/home.html', {'event_details': event_details})

# __________--- Get info for json file ---___________#
def edit_event(request):
    if request.method == 'POST':
        form = EventDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('events.views.home'))
        else:
            error = 'There seems to be an error. Please fill all the fields and submit the form again.'
            form = EventDetailsForm()
            return render_to_response('events/editEvent.html', {'error': error, 'form': form}, context_instance = RequestContext(request))
    else:
        form = EventDetailsForm()
    return render_to_response('events/editEvent.html', {'form': form}, context_instance = RequestContext(request))

def add_update(request):
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('events.views.home'))
        else:
            error = 'There seems to be an error. Please fill all the fields and submit the form again.'
            form = UpdateForm()
            return render_to_response('events/update.html',{'error': error, 'form': form}, context_instance = RequestContext(request))
    else:
        form = UpdateForm()
    return render_to_response('events/update.html',{'form': form}, context_instance = RequestContext(request))

def tabfile_submit(request):
    if request.method == 'POST':
        form = UploadTabFiles(request.POST, request.FILES)
        filename = request.FILES['tab_file'].name
        display_name = request.META['HTTP_X_NAME']
        print display_name
        
    else:
        form = UploadTabFiles()
    return render_to_response('events/tabfiles.html',{'form':form}, context_instance = RequestContext(request))
    

