from django import forms

class EventDetailsForm(forms.Form):
    name = forms.CharField(max_length=50, help_text='The event name can have maximum of 50 letters')
    description = forms.CharField(widget=forms.Textarea)
    update = forms.CharField(max_length=200, help_text='The update should be less than 200 letters')
