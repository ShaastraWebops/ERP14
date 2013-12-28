from django import forms 
from django.forms import ModelForm 
from hospi.models import *

class AddRoomForm(ModelForm):
    class Meta:
        model = AvailableRooms
        exclude = ('already_checkedin','mattresses',)

class IndividualForm(ModelForm):
    class Meta:
        model = IndividualCheckIn
        fields = ('room',
                'duration_of_stay',
                'number_of_mattresses_given',
                'mattress_room',
                'shaastra_ID',
                'check_in_control_room',
                'check_out_control_room',
                'comments',
                )


class ShaastraIDForm(forms.Form):
    shaastraID = forms.CharField(required=False,help_text='Enter Shaastra ID')
