from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .models import files_model

class UploadFileForm(forms.ModelForm):	
    class Meta :
        model = files_model
        exclude = ('user',)
    def clean_attachment(self):
        content = self.cleaned_data['attachment']
        content_type = content.content_type
        if content_type in settings.CONTENT_TYPES:
            if content._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep image size under %s. Current imagesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
        else:
            raise forms.ValidationError(_('Image type is not supported'))
        return content
    def clean_events_sponsor(self):
        sponsor_type = self.cleaned_data['sponsor_type']
        events_sponsor = self.cleaned_data['events_sponsor']
        if sponsor_type == 'events_spons':
             if events_sponsor:
                return events_sponsor
             else:
                raise forms.ValidationError(_('please fill in this column if you are uploading events sponsor image or change Sponsor_type if not'))
        else:
            if events_sponsor:
                  raise forms.ValidationError(_('please disable this column if you are uploading general sponsor image or change Sponsor_type if not'))
        return events_sponsor
class EditTitleForm(forms.ModelForm):
    class Meta:
        model = files_model
        exclude = ('user','attachment',)
    def clean_events_sponsor(self):
        sponsor_type = self.cleaned_data['sponsor_type']
        events_sponsor = self.cleaned_data['events_sponsor']
        if sponsor_type == 'events_spons':
             if events_sponsor:
                return events_sponsor
             else:
                raise forms.ValidationError(_('please fill in this column if you are uploading events sponsor image or change Sponsor_type if not'))
        else:
            if events_sponsor:
                  raise forms.ValidationError(_('please disable this column if you are uploading general sponsor image or change Sponsor_type if not'))
        return events_sponsor
