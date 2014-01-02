from django.db import models
# Create your models here.
from events.models import GenericEvent
#TODO: each of there shaastra id's to be converted to links to mainsite db!!

class Barcode(models.Model):
    #uprofile = models.ForeignKey(UserProfile,unique = False)
    shaastra_id = models.CharField(max_length = 40,unique = False)
    barcode = models.CharField(max_length = 100)
    def __unicode__(self):
        return "ID: %s; Barcode:%s" % (self.shaastra_id,self.barcode)
    #TODO: barcode is string of length ?

class Event_Participant(models.Model):
    event = models.ForeignKey(GenericEvent)
    shaastra_id = models.CharField(max_length = 40)
    def __unicode__(self):
        return "ID: %s; Event:%s" % (self.shaastra_id,self.event.title)
    
    
class Insti_Participant(models.Model):
    event = models.ForeignKey(GenericEvent)
    insti_roll = models.CharField(max_length = 10)
    
class PPM(models.Model):
#One-many or one-one?? Temporarily kept at the safer option - one-many.
    event = models.ForeignKey(GenericEvent)
    first_prize_winners  =  models.ManyToManyField (Barcode, blank = True, null = True, related_name='firstprize_set' )
    second_prize_winners =  models.ManyToManyField (Barcode, blank = True, null = True, related_name='secondprize_set')
    third_prize_winners =  models.ManyToManyField (Barcode, blank = True, null = True, related_name='thirdprize_set')
    need_consoling       =  models.ManyToManyField (Barcode, blank = True, null = True, related_name='consolation_set')
    
