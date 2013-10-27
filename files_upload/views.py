# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.files.storage import default_storage
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm 
from .models import files_model
@login_required
def upload_file(request):
    user=request.user
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
    #only allows files only in jpg format
        if form.is_valid():
            title=request.POST['title']
            check=files_model.objects.filter(title=title)#uncomment this after implementing login,user=user)
            if check:
                error='Please select another title for your file, it has already been used'
            else:
                form.save()
                #files will be uploaded inside media folder(MEDIA_ROOT/varun)
                message='Your upload has been successful, please select a file to upload again'
    else:
        form = UploadFileForm()
        message='Select a file to upload'
    return render_to_response('files_upload/upload.html', locals(), context_instance=RequestContext(request))


