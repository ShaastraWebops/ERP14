# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.files.storage import default_storage
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

# Imaginary function to handle an uploaded file.
#from .handle_file_upload import handle_uploaded_file
from .forms import UploadFileForm,EditTitleForm
from .models import files_model


@login_required
def upload_file(request):
    user=request.user
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
    #only allows files only in pdf format
        if form.is_valid():
            title=request.POST['title']
            attachment=request.FILES['attachment']
            sponsor_type=request.POST['sponsor_type']
            events_sponsor=request.POST['events_sponsor']
            check=files_model.objects.filter(title=title,user=user)
            if check:
                error='Please select another title for your file, it has already been used'
            else:
                doc = files_model(title=title,user=user,sponsor_type=sponsor_type,events_sponsor=events_sponsor,attachment=attachment)
                doc.save()
                #files will be uploaded inside media folder(MEDIA_ROOT/varun)
                message='Your upload has been successful, please select a file to upload again'
    else:
        form = UploadFileForm()
        message='Select a file to upload'
    return render_to_response('files_upload/upload.html', locals(), context_instance=RequestContext(request))


@login_required
def list_of_spons(request):
    user=request.user
    photos = files_model.objects.filter(user=user)
    return render_to_response('files_upload/list.html',locals(), context_instance=RequestContext(request))
@login_required
def edit_title(request,pk):
    user=request.user
    print(user)
    if pk:
        try:
            orig_logo=files_model.objects.get(id=pk,user=user)
        except:
            return HttpResponseRedirect('/files_upload/list')
        if request.method == 'POST':
            form = EditTitleForm(request.POST, request.FILES, instance=orig_logo)
            if form.is_valid():
                title=request.POST['title']
                logos=files_model.objects.filter(title=title,user=user)
                print(logos)
                for new_logo in logos:
                    print(new_logo)
                    if new_logo.id!=pk:
                        error="please choose another title,this title is already used"
                        print(error)
                        return render_to_response('files_upload/edit_title.html',locals(), context_instance=RequestContext(request)) 
                form.save()
                message="success"
        else:
            form=EditTitleForm(instance=orig_logo)
            message="edit the title"
        return render_to_response('files_upload/edit_title.html',locals(), context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('upload_file')
       
