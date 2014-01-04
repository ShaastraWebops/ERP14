from django import forms
from events.models import GenericEvent
from users.models import *
from models import *
EVENT_CHOICES = ((event.title,event.title) for event in GenericEvent.objects.all())
COLLEGE_CHOICES = ((college.name +"|"+ college.city+"|" + college.state,college.name +"|"+ college.city+"|" + college.state) for college in College.objects.using('mainsite').all().order_by('name'))

class BarcodeForm(forms.ModelForm):
    class Meta:
        model = Barcode

class Event_Participant_Form(forms.ModelForm):
    class Meta:
        model = Event_Participant

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length = 50,min_length = 1)
    email = forms.EmailField()
    last_name = forms.CharField(max_length = 50,min_length = 1)

    coll = forms.ChoiceField(choices = COLLEGE_CHOICES,help_text = 'Try to find the college here, else fill form below')
    class Meta:
        model = UserProfile

        fields = ('branch','mobile_number','gender','age','shaastra_id')
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

class Winner1Form(forms.Form):
    shaastra1_id1 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    
    shaastra1_id2 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    
    shaastra1_id3 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra1_id4 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra1_id5 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra1_id6 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)

class Winner2Form(forms.Form):
    shaastra2_id1 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    
    shaastra2_id2 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    
    shaastra2_id3 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra2_id4 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra2_id5 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra2_id6 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)

class Winner3Form(forms.Form):
    shaastra3_id1 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    
    shaastra3_id2 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    
    shaastra3_id3 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra3_id4 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra3_id5 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra3_id6 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
class Winner4Form(forms.Form):
    shaastra4_id1 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    
    shaastra4_id2 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    
    shaastra4_id3 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra4_id4 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra4_id5 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra4_id6 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
class Winner5Form(forms.Form):
    shaastra5_id1 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    
    shaastra5_id2 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    
    shaastra5_id3 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra5_id4 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra5_id5 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra5_id6 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
class Winner6Form(forms.Form):
    shaastra6_id1 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    
    shaastra6_id2 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    
    shaastra6_id3 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra6_id4 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra6_id5 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    shaastra6_id6 = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
    

class DetailForm(forms.Form):
    shaastra_id = forms.CharField(help_text = 'Enter shaastra ID of participant here',max_length = 10,required= False)
