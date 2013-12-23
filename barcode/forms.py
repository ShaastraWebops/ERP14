from django import forms
from events.models import GenericEvent

EVENT_CHOICES = ((event.title,event.title) for event in GenericEvent.objects.all())



class UploadFileForm(forms.Form):
    file  = forms.FileField()
    title = forms.CharField(help_text = "Enter the column name in excel sheet.Do not make spelling mistakes.",max_length = 50)


class EventForm(forms.Form):
    event_title = forms.ChoiceField(choices=EVENT_CHOICES,
                             help_text='Choose the event for which list is being uploaded. Please check twice'
                             )

