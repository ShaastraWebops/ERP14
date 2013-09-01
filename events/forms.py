# Basic Django form
from django import forms
from django.forms import ModelForm, Select
# From erp
from erp.settings import MEDIA_ROOT
from erp.variables import events_being_edited
# From form
from events.models import GenericEvent, AudienceEvent, ParticipantEvent, Tab, Update, TabFile
# Python imports
import json
import os, glob
import datetime

# __________--- Get place to store JSON - for events ---___________#
def get_json_file_path(filename):
    file_path = os.path.abspath( os.path.join( MEDIA_ROOT, 'json', 'events') )
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return os.path.join(file_path, filename)
    
# __________--- Exception in case of concurrent editing of the JSON file ---___________#
class EditError(Exception):
    '''
       This is the (custom) exception that is raised in case any error occurs during form saving.
    '''
    def __init__(self, value):
        self.value = value
        
def save_event(self, EventDetailsForm):
    '''
        Args:
        self - instance of the object that calls this function (this function is supposed to behave as a method)
        EventDetailsForm - the form to be edited
        
        Local vars:
        event_json - dict that holds data from the form
        json_data - data (python dict) loaded from the JSON file
        file_path_full - path pointing to the JSON file
        
        This fucntion does the following (in the given order):
        -> saves the ModelForm to the db.
        -> finds all files with name starting with the pk of the saved event, in media/json/events directory.
           (ideally only one or no such file should exist) If the found filename doesnt match the new filename (submitted in the form),
           it renames the found filename to new filename.
           In case there are more than one files found starting with the same pk, then there is some error, it removes all such files.
        -> If a file is found in the above step, then only the fields starting with 'event_' are changed (to avoid altering tab data).
           If no file exists, then a new file is created, which contains the event data.
        -> before editing the file, the function checks if the event_pk is present in events_being_edited. If yes, EditError is raised.
    '''
    clean_form = self.clean()
    event_json = {}
    json_data = {}
    
    # saving the event to db
    event_inst = super(EventDetailsForm, self).save()
    
    #event_pk = GenericEvent.objects.filter(title=clean_form['title'])[0].pk
    event_pk = event_inst.pk
    for iden in self.fields.keys(): # take all fields in the form
        event_json['event_'+iden] = clean_form[iden] # add to json
    # absolute path to the file in which the content has to be saved
    file_path_full = get_json_file_path(str(event_pk)+'_'+clean_form['title']+'.json')
    
    # rename the old file (that starts with this event_pk) to the new filename incase the event name has changed
    file_path_pk = get_json_file_path(str(event_pk)+'_*')
    file_path = glob.glob(file_path_pk) # gives all files in the dir that start with file_path_pk -- ideally returns only a single file
    if len(file_path)==1 :
        if not (file_path[0] == file_path_full):
            os.rename(file_path[0], file_path_full)
    elif len(file_path)>1 : # if there are more than one files starting with this pk, there is some error. Delete all these files.
        for path in file_path:
            if not (path == file_path_full):
                os.remove(path)
    
    if os.path.exists(file_path_full):
        with open(file_path_full) as f:
            json_data = json.load(f)
            for key in event_json.keys():
                json_data[key] = event_json[key]
            f.close()
    else:
        json_data = event_json
            
    if event_pk in events_being_edited:
        raise EditError('Event is being edited by some other user. Please try again later')
    
    events_being_edited.append(event_pk)
    with open(file_path_full, 'w') as f:
        json.dump(json_data, f)
        f.close()
        events_being_edited.remove(event_pk)
    return True

class GenericEventDetailsForm(ModelForm):
    #name = forms.CharField(max_length=50, help_text='The event name can have maximum of 50 letters')
    #description = forms.CharField(widget=forms.Textarea)
    #update = forms.CharField(max_length=200, help_text='The update should be less than 200 letters')

    class Meta:
        model = GenericEvent
        fields = ['title', 'category']
        
    def save(self, commit=True):
        save_event(self, EventDetailsForm)

class AudienceEventDetailsForm(ModelForm):
    
    class Meta:
        model = AudienceEvent
        exclude = ('event_type', 'events_logo', 'spons_logo', 'tags')
        
    def save(self, commit=True):
        save_event(self, AudienceEventDetailsForm)
        
class ParticipantEventDetailsForm(ModelForm):
    
    class Meta:
        model = ParticipantEvent
        exclude = ('event_type', 'events_logo', 'spons_logo', 'tags')
        
    def save(self, commit=True):
        save_event(self, ParticipantEventDetailsForm)
        
  
class TabDetailsForm(ModelForm):

    class Meta:
        model = Tab
        fields = ['title', 'text', 'pref']
    
    def save(self, event_inst = None, commit=True):
        '''
            event_inst - instance of event the tab belongs to. must exist as tab cannot exist without an event.
        '''
        clean_form = self.clean()
        json_data = {}
        # Save the tab to db
        tab_inst = super(TabDetailsForm, self).save()
        
        # Add event to the tab
        if event_inst:
            tab_inst.event = event_inst
            tab_inst.save()
        else:
            raise EditError('The tab must be linked to an event.')
        tab_pk = tab_inst.pk
        
        event_pk = event_inst.pk
        file_path = get_json_file_path(str(event_pk) + '_' + event_inst.title+'.json')
        if not os.path.exists(file_path): # No event file found- error: tab cant exist without the corresponding event
            raise EditError('Tab cannot be created without creating an event')
        with open(file_path) as f:
            json_data = json.load(f)
            for iden in self.fields.keys(): # take all fields in the form
                #print iden, clean_form[iden]
                json_data['tab'+str(tab_pk)+'_'+iden] = clean_form[iden] # add to existing json_data
                f.close()
            #return json_data
        
        if event_pk in events_being_edited:
            raise EditError('Event is being edited by some other user. Please try again later')
        
        events_being_edited.append(event_pk)
        with open(file_path, 'w') as f:
            json.dump(json_data, f)
            f.close()
            events_being_edited.remove(event_pk)
        return True

class UpdateForm(ModelForm):
    
    class Meta:

        model = Update
        exclude = ('date',)
        #widgets = {'event':forms.HiddenInput()}

    def save(self):
        clean_form = self.clean()
        date = datetime.datetime.now().strftime(' %d_%B_%I_%M%p')

        update_json = {}
        for iden in self.fields.keys():
            print iden, clean_form[iden]
            if iden == 'event':
                update_json[iden] = clean_form[iden].title
            else:
                update_json[iden] = clean_form[iden]
        file_path = get_json_file_path(clean_form['event'].title +date+'.json')
        print update_json
        with open(file_path, 'w') as f:
            json.dump(update_json, f)
            f.close()
        return True

class UploadTabFiles(ModelForm):

    class Meta:
        model = TabFile
        exclude = ('tab','url')
