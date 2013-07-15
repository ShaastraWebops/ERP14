# Basic Django form
from django import forms
from django.forms import ModelForm, Select
# From erp
from erp.settings import MEDIA_ROOT
from erp.variables import events_being_edited
# From form
from events.models import GenericEvent, Tab, Update, TabFile
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
    def __init__(self, value):
        self.value = value

class EventDetailsForm(ModelForm):
    #name = forms.CharField(max_length=50, help_text='The event name can have maximum of 50 letters')
    #description = forms.CharField(widget=forms.Textarea)
    #update = forms.CharField(max_length=200, help_text='The update should be less than 200 letters')

    class Meta:
        model = GenericEvent
        fields = ['title', 'category']
    
    def save(self, commit=True):
        clean_form = self.clean()
        event_json = {}
        json_data = {}
        
        # saving the event to db
        super(EventDetailsForm, self).save()
        
        event_pk = GenericEvent.objects.filter(title=clean_form['title'])[0].pk
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
        
class TabDetailsForm(ModelForm):

    class Meta:
        model = Tab
        fields = ['title', 'text', 'pref']
    
    def save(self, event_inst = None, commit=True):
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
