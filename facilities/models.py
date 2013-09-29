from django.db import models

from users.models import ERPUser

# Create your models here.

#_________---FACILITY ITEM (An available facility item on the menu)---________
class FacilityItem(models.Model):
    name = models.CharField(max_length=300)
    def __unicode__(self):
        return self.name


class FacilityOrder(models.Model):
    datecreated = models.DateTimeField ('Date Created', auto_now_add = True )
    dateapproved = models.DateTimeField ('Date Approved', blank=True, null=True)
    isapproved = models.BooleanField(default = False)
    items = models.ManyToManyField (FacilityItem, through='ItemEntry')
    creator = models.ForeignKey (ERPUser, related_name='facilityorder_created_set')
    approver = models.ForeignKey (ERPUser, related_name='facilityorder_approved_set', blank=True, null=True)
    


class ItemEntry(models.Model):
    order = models.ForeignKey (FacilityOrder)
    facilityitem = models.ForeignKey (FacilityItem)
    quantity = models.IntegerField(default=0)
    description = models.TextField('Description', blank=True, null=True)
    feedback = models.TextField('Description', blank=True, null=True)
    