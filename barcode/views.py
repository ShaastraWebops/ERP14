# Create your views here.
import csv
from django.shortcuts import render_to_response
from barcode.forms import UploadFileForm,EventForm
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse

def upload_csv(request, type):
    flag_str = ''
    print '!!!!!'+str(request.FILES)+'!!!!!'
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        event = EventForm(request.POST)
        #TODO: get event model from this...
        if form.is_valid() and event.is_valid():
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
            i=i+1
    if type_str == "participantsportal":
        if event_title == None:
            return False
        print event_title + "!!!!!!!!!!!"
        barcode = []
        for d in input_file:
            barcode.append(d[title])
        i=0
        while i<len(barcode):
            print barcode[i]+"||"
            i=i+1




#View to add an entry one at a time.
def add_single_entry(request):
    if type == "barcodeportal":
        title = "Barcode Portal"
        
        
    if type == "participantsportal":
        title = "Participant's Portal"
        #Needs work



#Function to process each user entry dictionary for the Barcode Portal
def barcodeportal_processor(entry):
    #Needs Work
    #
    #Placeholder:
    print entry['field1']
    print " "
    print entry['field2']
    print "\n"


#Function to process each user entry dictionary for the Participants Portal
def participantsportal_processor(entry):
    #Needs Work
    #
    #Placeholder:
    print entry['field1']
    print " "
    print entry['field2']
    print "\n"
