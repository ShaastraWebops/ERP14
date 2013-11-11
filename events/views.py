from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from events.forms import GenericEventDetailsForm,UpdateForm,UploadTabFiles,UploadFileForm
from events.models import UploadFile
from dashboard.models import TeamEvent
from users.models import UserProfile
from misc.dajaxice.core import dajaxice_functions
from erp.settings import DATABASES
mainsite_db = DATABASES.keys()[1]
import os
import csv
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
        form = GenericEventDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('events.views.home'))
        else:
            error = 'There seems to be an error. Please fill all the fields and submit the form again.'
            form = GenericEventDetailsForm()
            return render_to_response('events/editEvent.html', {'error': error, 'form': form}, context_instance = RequestContext(request))
    else:
        form = GenericEventDetailsForm()
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
    

def upload_file(request):

    curruser = request.user.get_profile()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST['title']
            title_exists = UploadFile.objects.filter(title = title)
            if title_exists:
                error = 'Given Title already exists'
            else:
                uploaded_file = UploadFile(title = title,upload_file = request.FILES['upload_file'])
                uploaded_file.event = curruser.event
                uploaded_file.title = title
                uploaded_file.save()
                message = "File Uploaded Successfully"
                return HttpResponseRedirect('')
    else:
        form = UploadFileForm()
        message = 'Select a File to upload'

    files_for_event = UploadFile.objects.filter(event = curruser.event)
    return render_to_response('events/upload_file.html',locals(),context_instance = RequestContext(request))

def registered_participants(request,exportCSV=False):
    curruser = request.user.get_profile()
    event_pk = curruser.event.pk
    teameventlist = TeamEvent.objects.using(mainsite_db).filter(event_id = event_pk)
    userlist =[]
    for team in teameventlist:
        userlist.append([team.users.all(),team.team_name])
    if exportCSV:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="participants.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name','Username','Email','Shaastra_ID'])
        for user1,team_name in userlist:
            for all_users in user1:
                writer.writerow([all_users.first_name,all_users.username,all_users.email,team_name])
        print response
        return response
    else:
        return render_to_response('events/reg_part.html',locals(),context_instance = RequestContext(request))

    


