from django import forms 
from django.forms import ModelForm 
from hospi.models import *

class AddRoomForm(ModelForm):
    class Meta:
        model = AvailableRooms
        exclude = ('already_checkedin','mattresses',)


