from django import forms
from events.models import GenericEvent
from users.models import *
from models import *
EVENT_CHOICES = ((event.title,event.title) for event in GenericEvent.objects.all())
COLLEGE_CHOICES = ((college.name +"|"+ college.city+"|" + college.state,college.name +"|"+ college.city+"|" + college.state) for college in College.objects.using('mainsite').all())

class BarcodeForm(forms.ModelForm):
    class Meta:
        model = Barcode

class Event_Participant_Form(forms.ModelForm):
    class Meta:
        model = Event_Participant

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length = 50,min_length = 1)
    email = forms.EmailField()
    coll = forms.ChoiceField(choices = COLLEGE_CHOICES,help_text = 'Try to find the college here, else fill form below')
    class Meta:
        model = UserProfile

        fields = ('branch','mobile_number', 'college_roll','gender','age','shaastra_id')
class CollegeForm(forms.ModelForm):
    class Meta:
        model = College
        fields = ('name','city','state')


class UploadFileForm(forms.Form):
    file  = forms.FileField()


class EventForm(forms.Form):
    event_title = forms.ChoiceField(choices=EVENT_CHOICES,
                             help_text='Choose the event for which list is being uploaded. Please check twice'
                             )

class DetailForm(forms.Form):
    shaastra_id = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10)    
