# Create your views here.
import csv
from django.shortcuts import render_to_response
from barcode.forms import *
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from events.models import GenericEvent
from models import Barcode,Event_Participant, PPM
from django.contrib import messages
from users.models import UserProfile
from django.forms.models import modelform_factory




def is_valid_id(shid):
    up = get_userprofile(shid)
    if up is None:
        return False
    return True

def is_valid_insti_roll(roll):
    #TODO::
    if len(roll)==8 and roll[:2].isalpha() and roll[2:4].isdigit() and roll[4].isalpha() and roll[5:].isdigit():
        return True
    return False

def get_userprofile(shaastra_id = None):
    if shaastra_id is None:
        return None
    try:
        up = UserProfile.objects.using('mainsite').filter(shaastra_id = shaastra_id)[0]
    except:
        return None
    return up

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
                display_list = []
                fail_list = []
                message_str = "Successfully uploaded "
                if type == "participantsportal":
                    (display_list,fail_list) = process_csv(request,request.FILES['file'],form.cleaned_data['title'],type,event.cleaned_data['event_title'] )
                    if display_list:
                        message_str+=str(display_list[0])
                        display_list = display_list[1:]
                        message_str += "::"
                        message_str+=str(display_list)
                else:
                    (display_list,fail_list) = process_csv(request,request.FILES['file'],form.cleaned_data['title'] ,type)
                    message_str += str(len(display_list)) + "items;"
                    message_str += str(display_list[0:5])
                    if fail_list:
                        message_str += "||Failed: %s" % str(fail_list)
                    
                
                messages.success(request,"%s..."% (message_str))
                return HttpResponseRedirect(reverse(type))
        else:
            flag_str = "Invalid Upload"
    else:
        form = UploadFileForm(initial={'title': 'SHAASTRA ID'})
        eventForm = EventForm()

    if type == "barcodeportal":
        title = "Barcode Portal"
    if type == "participantsportal":
        title = "Participant's Portal"
        eventForm = EventForm()
    return render_to_response('barcode/upload_csv.html', {'eventForm':eventForm,'flag_str':flag_str,'form': form, 'type': type, 'title': title}, context_instance=RequestContext(request))


def process_csv (request,file, title,type_str,event_title = None):
    input_file = csv.DictReader(file,delimiter=',')
    return_list = []
    fail_list = []
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
                fail_list.append(sh_id[i])
                i = i+1
                continue
                #TODO: what??
            if Barcode.objects.filter(shaastra_id = sh_id[i]).count()==0:
                barcode_obj = Barcode(shaastra_id = sh_id[i],barcode = barcode[i])
                return_list.append(str(sh_id[i]))
                barcode_obj.save()
            else:
                i=i+1
                continue
                #TODO: code to do when shaastra ID is scanned second time..
            #TODO: write to a log text file that this happened..
            i=i+1
    if type_str == "participantsportal":
        if event_title == None:
            return False
        barcode = []
        insti_list = []#List of insti roll no.s
        for d in input_file:
            if is_valid_insti_roll(d['BARCODE']):
                insti_list.append(d['BARCODE'])
            else:
                barcode.append(d['BARCODE'])
        event_list = GenericEvent.objects.filter(title = event_title)
        return_list.append(str(event_title))
        if event_list.count() == 0:
            return False
        event = event_list[0]
        sh_id = []
        error_list = []
        #TODO: implement roll no, of insti
        #NOW, get shaastra id of corresponding barcodes, and error list appended if not found
        for code in barcode:
            try:
                sh_id.append(Barcode.objects.get(barcode = code).shaastra_id)
            except:
                error_list.append(code)
        i=0
        for roll in insti_list:
            insti_part = Insti_Participant(event = event,insti_roll = roll)
            insti_part.save()
            #TODO: what to do with roll?? store??
            
        while i<len(sh_id):
            #print barcode[i]+"||"
            ev_part = Event_Participant(event = event,shaastra_id = sh_id[i])
            return_list.append(str(sh_id[i]))
            ev_part.save()
            i=i+1
        if len(error_list):
            messages.warning(request,'%d values were invalid: some are:%s' % (len(error_list),error_list))
            #TODO: display error list??
            #return False
    return (return_list,fail_list)


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
                return HttpResponse("Enter valid event . Go <a href='/barcode/csv/add_single_barcode'>Back</a>")
            return HttpResponse("Enter valid event . Go <a href='/barcode/csv/add_single_participant'>Back</a>")
    else:
        if flag_bar:
            title = "Barcode Portal"
            form = BarcodeForm()
        else:
            title = "Participant's Portal"
            form = Event_Participant_Form()
    return render_to_response('barcode/upload_single.html', {'form':form,'flag_str':flag_str, 'type': type, 'title': title}, context_instance=RequestContext(request))


def add_single_barcode(barcodedata):
    shid = barcodedata['shaastra_id']
    code = barcodedata['barcode']
    if not is_valid_id(shid):
        return ''
    
    barcode_obj = Barcode(shaastra_id = shid,barcode = code)
    barcode_obj.save()
    return 'add single success'
    
def add_single_participant(event_participant_data):
    
    try:
       shid = Barcode.objects.get(shaastra_id = event_participant_data['shaastra_id']).shaastra_id
       #NOTE: here form's shaastra id is used to get the shaastra ID, it actually barcode
    except:
        return ''
    if not is_valid_id(shid):
        return ''
    
    ev_part = Event_Participant(event = event_participant_data['event'],shaastra_id = shid)
    ev_part.save()
    return 'add single success'



def upload_ppm(request):
    PPMForm = modelform_factory(PPM)
    if request.method == 'POST':
        form = PPMForm (request.POST)
        if form.is_valid():
            form.save()
            return redirect('barcode.views.upload_ppm')

    else:
        #Display Blank Form
        form = PPMForm()
        context = {'form': form}
    
    return render_to_response ('barcode/ppm.htm', {'form': form }, context_instance=RequestContext(request))