from django import forms
from django.forms import ModelForm

#Importing the FacilityItem Model
from facilities.models import FacilityItem

class FacilityItemForm(ModelForm):
    class Meta:
        model = FacilityItem