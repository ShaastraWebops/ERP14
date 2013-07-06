# Basic Django form
from django import forms
from django.forms import ModelForm, Select
# From erp
from erp.settings import MEDIA_ROOT
# From form
from events.models import GenericEvent, Tab, Update, TabFile
# Python imports
import json
import os
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
        for iden in self.fields.keys(): # take all fields in the form
            print iden, clean_form[iden]
            event_json[iden] = clean_form[iden] # add to json
        file_path = get_json_file_path(clean_form['title']+'.json')
        print event_json
        with open(file_path, 'w') as f:
            json.dump(event_json, f)
            f.close()
        return True
        
'''class TabDetailsForm(ModelForm):

    class Meta:
        model = Tab
        fields = ['event', 'title', 'text', 'pref']'''

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
