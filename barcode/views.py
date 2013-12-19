# Create your views here.
import csv
from django.shortcuts import render_to_response
from barcode.forms import UploadFileForm
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def upload_csv(request, type):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            process_csv (request.FILES['file'], type)
            return HttpResponseRedirect(reverse(type))
    else:
        form = UploadFileForm()

    if type == "barcodeportal":
        title = "Barcode Portal"
    if type == "participantsportal":
        title = "Participant's Portal"

    return render_to_response('barcode/upload.html', {'form': form, 'type': type, 'title': title}, context_instance=RequestContext(request))




def process_csv (file, type):
    input_file = csv.DictReader(file)
    
    if type == "barcodeportal":
        #Set field names here
        input_file.fieldnames = "field1", "field2"

        for entry in input_file:
            barcodeportal_processor(entry)

    if type == "participantsportal":
        #Set field names here
        input_file.fieldnames = "field1", "field2"

        for entry in input_file:
            participantsportal_processor(entry)




#View to add an entry one at a time.
def add_single_entry(request):
    if type == "barcodeportal":
        title = "Barcode Portal"
        #Needs work
        
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