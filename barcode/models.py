from django.db import models
# Create your models here.
from events.models import GenericEvent
class Barcode(models.Model):
    #uprofile = models.ForeignKey(UserProfile,unique = False)
    shaastra_id = models.CharField(max_length = 40)
    barcode = models.CharField(max_length = 100)
    #TODO: barcode is string of length ?

class Event_Participate(models.Model):
    event = models.ForeignKey(GenericEvent)
    shaastra_id = models.CharField(max_length = 40)
