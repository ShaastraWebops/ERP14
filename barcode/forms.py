from django import forms
from events.models import GenericEvent
from models import *
EVENT_CHOICES = ((event.title,event.title) for event in GenericEvent.objects.all())

class BarcodeForm(forms.ModelForm):
    class Meta:
        model = Barcode

class Event_Participant_Form(forms.ModelForm):
    class Meta:
        model = Event_Participant


class UploadFileForm(forms.Form):
    file  = forms.FileField()
    title = forms.CharField(help_text = "Enter the column name in excel sheet.If you are following standard format, just leave this as SHAASTRA ID",max_length = 50)


class EventForm(forms.Form):
    event_title = forms.ChoiceField(choices=EVENT_CHOICES,
                             help_text='Choose the event for which list is being uploaded. Please check twice'
                             )

class DetailForm(forms.Form):
    shaastra_id = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10)    
