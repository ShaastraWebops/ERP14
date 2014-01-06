from users.models import UserProfile, College
from django.contrib.auth.models import User
#from events.models import Event, EventSingularRegistration
from barcode.models import Barcode,Event_Participant,Certis
#from prizes.models import BarcodeMap
from events.models import GenericEvent
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseForbidden, HttpResponse
from barcode.scripts import *

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase.pdfmetrics import getFont, getAscentDescent
from reportlab.platypus import Paragraph, Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
    
import datetime

def log(msg):

    destination = open('/home/shaastra/hospi/certis/log.txt', 'a')
    destination.write(str(msg))
    destination.write('\n')
    destination.close()
#    print msg

def PDFSetFont(pdf, font_name, font_size):
    """
    Sets the font and returns the lineheight.
    """

    pdf.setFont(font_name, font_size)
    (ascent, descent) = getAscentDescent(font_name, font_size)
    return ascent - descent  # Returns line height

def paintImage(pdf, x, y, im):

    (A4Width, A4Height) = A4
    availableWidth = A4Width - 2 * cm  # Leaving margins of 1 cm on both sides
    availableHeight = y
    (imWidth, imHeight) = im.wrap(availableWidth, availableHeight)  # find required space
    
    im.drawOn(pdf, x, y - imHeight)
    
    x -= imWidth + cm
    y -= imHeight + cm
    
    return (x, y)
    
def constructName(user):
    name = ''
    if user.first_name or user.last_name:
        if user.first_name:
            name += user.first_name
        if user.last_name:
            if len(name) > 0:
                name += ' '
            name += user.last_name
        name = name.title()
    else:
        log('User %s (%d) does not have a first/last name.' % (user.username, user.id))
        name += user.username
    return name    

def generateCertificate(user,event_name):
    try:
        userProfile = UserProfile.objects.using('mainsite').get(user = user)
    except:
        
        return None
    """
    if event.__class__.__name__!='GenericEvent':
        return None
    """
    # Create a buffer to store the contents of the PDF.
    # http://stackoverflow.com/questions/4378713/django-reportlab-pdf-generation-attached-to-an-email
    buffer = StringIO()
    
    CS = (3508, 2480)  # Certificate [Page] Size
    #CS = landscape(A4)

    # Create the PDF object, using the response object as its "file."

    pdf = canvas.Canvas(buffer, pagesize=CS)

    # Get the width and height of the page.

    (pageWidth, pageHeight) = CS
    
    y = pageHeight
    x = 0
    
    im = Image("/home/shaastra/hospi/certis/certback_final.jpg")
    im.hAlign = 'LEFT'
    
    paintImage(pdf, x, y, im)
    
    # Set font for Participant Name
    lineheight = PDFSetFont(pdf, 'Times-Bold', 80)
    xuser = (30.8 + (65.54/2))*cm
    yuser = 45.62*cm + lineheight
    name = constructName(user)
    pdf.drawString(xuser, yuser, '%s' % name)
    xevent = (24.3 + (65.54/2))*cm
    yevent = 37.62*cm + lineheight
    ename = event_name
    pdf.drawString(xevent, yevent, '%s' % ename)
    
    
    pdf.showPage()
    pdf.save()

    response = buffer.getvalue()
    buffer.close()

    return response
    
def mailPDF(user, pdf):
    return
    subject = 'Participation Certificate (Corrected), Shaastra 2014'
    message = 'PFA the <b>corrected</b> certificate. <br/><br/>Team Shaastra 2014<br/>'
    email = user.email
    #email = 'swopstesting@gmail.com' #TODO: Remove this line for finale

    msg = EmailMultiAlternatives(subject, message, 'noreply@iitm.ac.in' , [email,])
    msg.content_subtype = "html"
    msg.attach('%s-certificate.pdf' % user.get_profile().shaastra_id, pdf, 'application/pdf')
    msg.send()  #TODO: Uncomment this line for finale
    log('Mail sent to %s' % email)  #TODO: Uncomment this line for finale
    #log('NOT sent. Mail will go to %s' % email)  #TODO: Comment this line for finale
    
def savePDF(pdf, user,ename):
    try:
        profile = UserProfile.objects.using('mainsite').get(user = user)
    except:
        return
    destination = open('/home/shaastra/hospi/certis/'+profile.shaastra_id+'_'+ename+'-certificate.pdf', 'wb+')
    destination.write(pdf)
    destination.close()
    log('File '+profile.shaastra_id+'-certificate.pdf saved.')

def cookAndServeCertis():
    
    #return ('Comment this line to send the Participant PDFs.')
    
    log('\n\n**********  Now: %s  **********' % datetime.datetime.now())
    participants = []
    uids = []
    shids_event = []
    for ep in Event_Participant.objects.all():
        try:
            Certis.objects.get(ep = evp)
        except:
            shids_event.append((ep.shaastra_id,ep.event))
            Certis.objects.create(ep = ep,done = True)
    # remove ID's not in DB, and junk userprofiles
    shids_event = [(shid_event[0],shid_event[1]) for shid_event in shids_event if id_in_db(shid_event[0])]
    shids_event = [(shid_event[0],shid_event[1]) for shid_event in shids_event if not is_junk(shid_event[0])]
    print str(shids_event)
    print len(shids_event)
    for shid_event in shids_event:
        log(shid_event[0] + "event" +str(shid_event[1]))
        if shid_event[1]:
            pdf = generateCertificate(get_userprofile(shid_event[0]).user,shid_event[1].title)
        else:
            continue
        if get_userprofile(shid_event[0]).user.email:
            #mailPDF(participant, pdf)
            savePDF(pdf, get_userprofile(shid_event[0]).user,shid_event[1].title)
        
            
    
#    for participant in participants:
#        log(participant.id)
#        pdf = generateCertificate(participant,"Chuck Glider Workshop prelims")
#        if pdf is None:
#            print '#**&#*&'
#            continue
#        if participant.email:
#            #mailPDF(participant, pdf)
#            savePDF(pdf, participant)
#            #break  #TODO: Remove this for the finale

