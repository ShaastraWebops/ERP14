from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django import forms
from django.db import models
ALLOWED_FILETYPE = ['doc','pdf','odt','txt']

def tdp_upload_handler(self,filename):
#    time =  strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()).replace(" ",'_')
    time = str(timezone.now().date())
    fname = str(filename).split('.')[-1]
    if (fname.split('.')[-1] not in ALLOWED_FILETYPE):
        raise forms.ValidationError("File type is not supported.")
    url = 'tdpsubmissions/%s/%s_%s'%(self.teamevent.get_event().title,self.teamevent.team_id,time)
    return url


class TeamEvent(models.Model):
    team_id     = models.CharField(default='0',null=True,max_length = 50)
    team_name   = models.CharField(max_length = 30,blank = True,null=True)
    users       = models.ManyToManyField(User, blank = True, null = True)
    is_active   = models.BooleanField(default = False)
    #permissions = models.ManyToManyField(Permission, blank = True, null = True)
    event_id       = models.IntegerField(default=-1)#This will store id of participant event

class TDP(models.Model):
    teamevent   = models.ForeignKey(TeamEvent,null = True,blank = True)
    file_tdp    = models.FileField(max_length = 100,upload_to =tdp_upload_handler,blank=True,null=True)

    def get_event(self):
        try:
            event =  ParticipantEvent.objects.get(id = self.event_id)    
            return event
        except:
            return None
