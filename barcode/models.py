import csv
from django.db import models
# Create your models here.
from events.models import GenericEvent
from users.models import UserProfile
#TODO: each of there shaastra id's to be converted to links to mainsite db!!
#from scripts import get_userprofile
class Barcode(models.Model):
    #uprofile = models.ForeignKey(UserProfile,unique = False)
    shaastra_id = models.CharField(max_length = 40,unique = False)
    barcode = models.CharField(max_length = 100)
    def __unicode__(self):
        return "ID: %s; Barcode:%s" % (self.shaastra_id,self.barcode)
    def profiledata(self):
        try:
            profile =UserProfile.objects.using('mainsite').get(shaastra_id = self.shaastra_id)
            if profile.college:
                string = "Name:%s ;College:%s"%(profile.user.get_full_name(),profile.college.name)
            else:
                #return '!'+profile.user.get_full_name()+'!'
                if profile.user.get_full_name()!='Junk':
                    string = "Name:%s ;"%(profile.user.get_full_name())
                    
                else:
                    string = 'Insti_Participant: Name not provided'
        except:
            string = "failed to retrieve data"
        return string
    def save(self,*args,**kwargs):
        writecsv(self)
        super(self.__class__,self).save(*args,**kwargs)
    #TODO: barcode is string of length ?


def writecsv(barcode):
    b  = open('/home/shaastra/django-projects/Shaastra-2014/erp/media/barcode.csv','a')
#    b = open('~/django-projects/Shaastra2014/erp/media/barcode.csv','a')
    a = csv.writer(b)
    data = []
    
#    for barcode in Barcode.objects.all():
    data.append([barcode.barcode,'<--BARCODE SHID-->',barcode.shaastra_id])
    a.writerows(data)
    b.close()


    #TODO: barcode is string of length ?


def writecsv(barcode):
    b  = open('/home/shaastra/django-projects/Shaastra-2014/erp/media/barcode.csv','a')
#    b = open('~/django-projects/Shaastra2014/erp/media/barcode.csv','a')
    a = csv.writer(b)
    data = []
    
#    for barcode in Barcode.objects.all():
    data.append([barcode.barcode,'<--BARCODE SHID-->',barcode.shaastra_id])
    a.writerows(data)
    b.close()


class Event_Participant(models.Model):
    event = models.ForeignKey(GenericEvent)
    shaastra_id = models.CharField(max_length = 40)
    def __unicode__(self):
        return "ID: %s; Event:%s" % (self.shaastra_id,self.event.title)

class Certis(models.Model):
    ep = models.ForeignKey(Event_Participant)
    done = models.BooleanField(default = False)
    
class Insti_Participant(models.Model):
    event = models.ForeignKey(GenericEvent)
    insti_roll = models.CharField(max_length = 10)
    
class PrizeWinner(models.Model):
    position = models.IntegerField(default = 4)
    winners = models.ManyToManyField(Barcode,blank = True,null = True)
    event = models.ForeignKey(GenericEvent)
    def __unicode__(self):
        return self.event.title + '::winners'
