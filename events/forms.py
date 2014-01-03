# Basic Django form
from django import forms
from django.forms import ModelForm, Select
# From erp
from erp.settings import MEDIA_ROOT
from erp.variables import events_being_edited
# From form
from events.models import GenericEvent, AudienceEvent, ParticipantEvent, Tab, Update, TabFile,EVENT_CATEGORIES,UploadFile
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
    
def get_category_json_file_path(filename):
    file_path = os.path.abspath( os.path.join( MEDIA_ROOT, 'json') )
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

def datetime_handler(obj):
    return obj.strftime('%Y-%m-%d') if hasattr(obj,'isoformat') else obj

        
def save_event(self, EventDetailsForm):
    '''
        Args:
        self - instance of the object that calls this function (this function is supposed to behave as a method)
        EventDetailsForm - the form to be edited
        
        Local vars:
        event_json - dict that holds data from the form
        json_data - data (python dict) loaded from the JSON file
        file_path_full - path pointing to the JSON file
        event_title_new - new (changed) title of the event
        
        This fucntion does the following (in the given order):
        -> saves the ModelForm to the db.
        -> finds all files with name starting with the pk of the saved event, in media/json/events directory.
           (ideally only one or no such file should exist) If the found filename doesnt match the new filename (submitted in the form),
           it renames the found filename to new filename.
           In case there are more than one files found starting with the same pk, then there is some error, it removes all such files.
        -> If a file is found in the above step, then only the fields starting with 'event_' are changed (to avoid altering tab data).
           If no file exists, then a new file is created, which contains the event data.
        -> if the title of the event changes, then change the title of the event in event_category.json file (this file holds details about 
           all events belonging to each category)
        -> before editing the file, the function checks if the event_pk is present in events_being_edited. If yes, EditError is raised.
    '''
    clean_form = self.clean()
    event_json = {}
    json_data = {}
    event_title_new = None
    
    # saving the event to db
    event_inst = super(EventDetailsForm, self).save()
    
    #event_pk = GenericEvent.objects.filter(title=clean_form['title'])[0].pk
    event_pk = event_inst.pk
    for iden in self.fields.keys(): # take all fields in the form
        event_json['event_'+iden] = clean_form[iden] # add to json
    # absolute path to the file in which the content has to be saved
    file_path_full = get_json_file_path(str(event_pk)+'_'+clean_form['title']+'.json')
    
    # absolute path to json file which holds categories
    category_json_file_path = get_category_json_file_path('event_category.json')
    
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
            if json_data['event_title'] != event_json['event_title']:
                event_title_new = event_json['event_title']
            for key in event_json.keys():
                json_data[key] = event_json[key]
            f.close()
    else:
        json_data = event_json
    if event_pk in events_being_edited:
        print events_being_edited
        raise EditError('Event is being edited by some other user. Please try again later')

    
    events_being_edited.append(event_pk)
    with open(file_path_full, 'w') as f:
        json.dump(json_data, f,default=datetime_handler)
        f.close()
    
    if event_title_new and os.path.exists(category_json_file_path):
        with open(category_json_file_path) as f:
            category_json_data = json.load(f)
            # get the event_details from event_category.json file for the given event_pk
            event_details =  [ d for d in category_json_data[event_inst.category] if d['pk'] == event_pk ][0]
            event_details_index =  category_json_data[event_inst.category].index(event_details)
            event_details['title'] = event_title_new
            category_json_data[event_details_index] = event_details
            f.close()
        with open(category_json_file_path, 'w') as f:
            json.dump(category_json_data, f)
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
        exclude = ('event_type', 'events_logo', 'spons_logo', 'tags',)
   
    def __init__(self,*args,**kwargs):
        super(ParticipantEventDetailsForm, self).__init__(*args,**kwargs)
        self.fields['registration_starts'].help_text = 'Start Registration: YYYY-MM-DD'
        self.fields['registration_ends'].help_text = 'End Registration : YYYY-MM-DD'
        
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
        exclude = ('date','event')
        #widgets = {'event':forms.HiddenInput()}

    def save(self, event_inst,update_pk=None):
        clean_form = self.clean()
        json_data = {}
        if update_pk:
            update_inst = super(UpdateForm, self).save()
            update_inst.pk = update_pk
            update_inst.event = event_inst
            update_inst.save()
        else:
            update_inst = super(UpdateForm, self).save()
            update_inst.event = event_inst
            update_inst.save()
        event_pk = event_inst.pk
        update_pk = update_inst.pk
        
        #date = datetime.datetime.now().strftime(' %d_%B_%I_%M%p')
        file_path = get_json_file_path(str(event_pk) + '_' +event_inst.title + '.json')
        if not os.path.exists(file_path):
            raise EditError('Update cannot be created without creating Event')
        with open(file_path) as f:
            json_data = json.load(f)
            for iden in self.fields.keys():
            #print iden, clean_form[iden]
                json_data['update'+str(update_pk)+'_'+iden] = clean_form[iden]

        if event_pk in events_being_edited:
            raise EditError('Event is being edited by some other user. Please try again later')
        events_being_edited.append(event_pk)
        with open(file_path,'w') as f:
            json.dump(json_data, f)
            f.close()
            events_being_edited.remove(event_pk)
        return True
                
        

class UploadTabFiles(ModelForm):

    class Meta:
        model = TabFile
        exclude = ('tab','url')

class ChooseEventForm(forms.Form):
    #event = forms.ModelChoiceField( queryset = GenericEvent.objects.all(), required=False)
    event_list = GenericEvent.objects.all()
    event_choices = [(event,event) for event in event_list]

    event = forms.ChoiceField(event_choices,required=False,widget=forms.Select())

class UploadFileForm(ModelForm):
    class Meta:
        model = UploadFile
        exclude = ('event',)
