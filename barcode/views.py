# Create your views here.
import csv
from django.shortcuts import render_to_response
from barcode.forms import *
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from events.models import GenericEvent
from models import Barcode,Event_Participant
from django.contrib import messages

def upload_csv(request, type):
    flag_str = ''
    
    eventForm = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        event = EventForm(request.POST)
        #TODO: get event model from this...
        if form.is_valid() and (type=="barcodeportal" or event.is_valid()):
            if not form.files:
                flag_str = 'Please upload a valid file'
                return HttpResponse(flag_str)
            elif not event and type=="participantsportal":
                flag_str = 'Choose a valid event'
                return HttpResponse(flag_str)
            else:
                if type == "participantsportal":
                    process_csv(request.FILES['file'],form.cleaned_data['title'],type,event.cleaned_data['event_title'] )
                else:
                    process_csv(request.FILES['file'],form.cleaned_data['title'] ,type)
                messages.success(request,"Successfully uploaded!")
                return HttpResponseRedirect(reverse(type))
        else:
            flag_str = "Invalid Upload"
    else:
        form = UploadFileForm()
        eventForm = EventForm()

    if type == "barcodeportal":
        title = "Barcode Portal"
    if type == "participantsportal":
        title = "Participant's Portal"
        eventForm = EventForm()
    return render_to_response('barcode/upload_csv.html', {'eventForm':eventForm,'flag_str':flag_str,'form': form, 'type': type, 'title': title}, context_instance=RequestContext(request))




def process_csv (file, title,type_str,event_title = None):
    input_file = csv.DictReader(file,delimiter=',')
    
    if type_str == "barcodeportal":
        sh_id = []
        barcode = []
        for d in input_file:
            sh_id.append(d[title])
            barcode.append(d['BARCODE'])
        i=0
        while i<len(sh_id):
            print sh_id[i]+"||"+barcode[i]+"__"
            if not is_valid_id(sh_id[i]):
                continue
                #TODO: what??
            barcode_obj = Barcode(shaastra_id = sh_id[i],barcode = barcode[i])
            barcode_obj.save()
            #TODO: write to a log text file that this happened..
            i=i+1
    if type_str == "participantsportal":
        if event_title == None:
            return False
        barcode = []
        for d in input_file:
            barcode.append(d['BARCODE'])
        event_list = GenericEvent.objects.filter(title = event_title)
        if event_list.count() == 0:
            return False
        event = event_list[0]
        sh_id = []
        error_list = []
        
        #NOW, get shaastra id of corresponding barcodes, and error list appended if not found
        for code in barcode:
            try:
                sh_id.append(Barcode.objects.get(barcode = code).shaastra_id)
            except:
                error_list.append(barcode)
        i=0
        while i<len(sh_id):
            #print barcode[i]+"||"
            ev_part = Event_Participant(event = event,shaastra_id = sh_id[i])
            ev_part.save()
            i=i+1
        if len(error_list):
            messages.warning(request,'%d values were invalid' % len(error_list))
            #TODO: display error list??
            #return False



#View to add an entry one at a time.
def add_single_entry(request,type):
    flag_bar = False
    flag_str = ''
    if type == "barcodeportal":
        flag_bar = True
    if request.method =='POST':
        if flag_bar:
            form = BarcodeForm(request.POST)
        else:
            form = Event_Participant_Form(request.POST)
        if form.is_valid():
            if flag_bar:
                flag_str = add_single_barcode(form.cleaned_data)
                if flag_str!='':
                    messages.success(request,'Successfully added')
                else:
                    messages.success(request,'Invalid data: Shaastra ID not valid')
                return HttpResponseRedirect(reverse('add_single_barcode'))

            else:
                flag_str = add_single_participant(form.cleaned_data)
                if flag_str !='':
                    messages.success(request,'Successfully added')
                else:
                    messages.success(request,'Invalid Shaastra ID: Not registered in Hospi Desk!!')
                return HttpResponseRedirect(reverse('add_single_participant'))
    else:
        if flag_bar:
            title = "Barcode Portal"
            form = BarcodeForm()
        else:
            title = "Participant's Portal"
            form = Event_Participant_Form()
    return render_to_response('barcode/upload_single.html', {'form':form,'flag_str':flag_str, 'type': type, 'title': title}, context_instance=RequestContext(request))


def is_valid_id(shid):
    #NEEDS WORK
    return True

def add_single_barcode(barcodedata):
    shid = barcodedata['shaastra_id']
    code = barcodedata['barcode']
    if not is_valid_id(shid):
        return ''
    
    barcode_obj = Barcode(shaastra_id = shid,barcode = code)
    barcode_obj.save()
    return 'cool'
    
def add_single_participant(event_participant_data):
    
    try:
       shid = Barcode.objects.get(barcode = event_participant_data['shaastra_id']).shaastra_id
       #NOTE: here form's shaastra id is used to get the shaastra ID, it actually barcode
    except:
        return ''
    if not is_valid_id(shid):
        return ''
    
    ev_part = Event_Participant(event = event_participant_data['event'],shaastra_id = shid)
    ev_part.save()
    return 'cool'
