# Basic Django form
from django import forms
from django.forms import ModelForm, Select
# From erp
from erp.settings import MEDIA_ROOT
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
            #print iden, clean_form[iden]
            event_json['event_'+iden] = clean_form[iden] # add to json
        # absolute path to the file in which the content has to be saved
        file_path_full = get_json_file_path(str(event_pk)+'_'+clean_form['title']+'.json')
        
        # removing all files except file_path_full that start with this event_pk
        file_path_pk = get_json_file_path(str(event_pk)+'_*')
        file_paths = glob.glob(file_path_pk) # gives all files in the dir that start with file_path_pk
        for path in file_paths:
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
                
        #print event_json
        with open(file_path_full, 'w') as f:
            json.dump(json_data, f)
            f.close()
        return True
        
class TabDetailsForm(ModelForm):

    class Meta:
        model = Tab
        fields = ['event', 'title', 'text', 'pref']
    
    def save(self, commit=True):
        clean_form = self.clean()
        json_data = {}
        #saving the tab to db
        super(TabDetailsForm, self).save()
        tab_pk = Tab.objects.filter(title=clean_form['title'])[0].pk
        
        event_pk = GenericEvent.objects.filter(title=clean_form['event'].title)[0].pk
        file_path = get_json_file_path(str(event_pk) + '_' + clean_form['event'].title+'.json')
        if not os.path.exists(file_path): # No event file found- error: tab cant exist without the corresponding event
            raise ValidationError(u'Tab cannot be created without creating an event')
        with open(file_path) as f:
            json_data = json.load(f)
            for iden in self.fields.keys(): # take all fields in the form
                #print iden, clean_form[iden]
                if iden=='event':
                    json_data['tab'+str(tab_pk)+'_'+iden] = clean_form[iden].title   # add event name to existing json_data
                else:
                    json_data['tab'+str(tab_pk)+'_'+iden] = clean_form[iden] # add to existing json_data
                f.close()
            #return json_data
        with open(file_path, 'w') as f:
            json.dump(json_data, f)
            f.close()
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
