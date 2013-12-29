from django.db import models
from datetime import datetime
from django.conf import settings
# from erp
from erp.settings import MEDIA_ROOT
from erp.variables import events_being_edited,venue_choices
from events.models import GenericEvent
# From form
#from events.forms import get_json_file_path, EditError
# python imports
import json
import os

class DTV(models.Model):
    venue = models.CharField(max_length = 50,choices = venue_choices)
    long_posn   = models.DecimalField (max_digits=9, decimal_places=4,blank = True,null=True)
    lat_posn   = models.DecimalField (max_digits=9, decimal_places=4,blank = True,null=True)
    events = models.ManyToManyField(GenericEvent,through = 'DTV_Event')
    def __unicode__(self):
        return self.venue + "::Lat-" + long_posn + "::Long-" + lat_posn
    
class DTV_Event(models.Model):
    dtv = models.ForeignKey(DTV)
    event = models.ForeignKey(GenericEvent)
    time_start = models.DateTimeField(auto_now=False, auto_now_add=False)
    time_end = models.DateTimeField(auto_now=False, auto_now_add=False)
    pre_regd = models.BooleanField(default = False)
