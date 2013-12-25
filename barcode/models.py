from django.db import models
# Create your models here.
from events.models import GenericEvent
#TODO: each of there shaastra id's to be converted to links to mainsite db!!

class Barcode(models.Model):
    #uprofile = models.ForeignKey(UserProfile,unique = False)
    shaastra_id = models.CharField(max_length = 40,unique = False)
    barcode = models.CharField(max_length = 100)
    #TODO: barcode is string of length ?

class Event_Participant(models.Model):
    event = models.ForeignKey(GenericEvent)
    shaastra_id = models.CharField(max_length = 40)
