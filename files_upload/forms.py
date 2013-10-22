from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .models import files_model

class UploadFileForm(forms.ModelForm):
    #title = forms.CharField(max_length=100,help_text='(add a title to your image)')
    #content  = forms.ImageField(help_text='(please keep file size below 5MB and give only imagess in jpg format)')	
    class Meta :
        model = files_model
    def clean_content(self):
        content = self.cleaned_data['content']
        content_type = content.content_type
        if content_type in settings.CONTENT_TYPES:
            if content._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep image size under %s. Current imagesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
        else:
            raise forms.ValidationError(_('Image type is not supported'))
        return content
    def clean_title(self):
        title=self.cleaned_data['title']
        check=files_model.objects.filter(title=title)#uncomment this after implementing login,user=user)
        if check:
            raise forms.ValidationError('This image name has already been used ,please choose another one')
        else:
            return title
