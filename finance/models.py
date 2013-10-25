from django.db import models
from users.models import ERPUser
from dept.models import Subdept, Dept
from events.models import GenericEvent


##BUDGETING MODELS##
class BudgetProposal(models.Model):
    creator = models.ForeignKey(ERPUser, related_name='created_budget_set')
    datecreated = models.DateField ('Date Created', auto_now_add = True )
    dateapproved = models.DateField (null=True, blank=True)
    
    event = models.ForeignKey(GenericEvent)
    
    comment = models.TextField()
    
    plan_1_total = models.IntegerField (default=0)
    plan_2_total = models.IntegerField (default=0)
    plan_1_description = models.TextField()
    plan_2_description = models.TextField()
    
    selectedplan = models.IntegerField (default=0)
    isapproved = models.BooleanField (default=False)
    approver = models.ForeignKey(ERPUser, related_name='approved_budget_set', null=True, blank=True)
    
    def __unicode__ (self):
        return '%s (%s)' %(self.event.title, self.creator)
        
        
        

##VOUCHERS MODELS####
class Vendor(models.Model):
    name = models.CharField ( max_length=30 )

    def __unicode__ (self):
        return self.name

class FinUniqueID(models.Model):
    value = models.CharField ( max_length=30 )
    vendor = models.ForeignKey ( Vendor )

    def __unicode__ (self):
        return self.value

class VoucherRequest(models.Model):
    datecreated = models.DateField ( 'Date Created', auto_now_add = True )
    dateapproved = models.DateField ( 'Date Approved', null=True, blank=True )
    amount = models.IntegerField ( default=0 )
    purpose = models.TextField ( null=True, blank=True )
    status = models.CharField ( max_length=1, choices = (( 'A', 'Approved' ),( 'P', 'Pending' )) )

    creator = models.ForeignKey ( ERPUser, related_name = 'voucherrequest_created_set' )
    approver = models.ForeignKey ( ERPUser, null=True, blank=True, related_name = 'voucherrequest_approved_set')    
    subdept = models.ForeignKey ( Subdept, blank=True, null=True )
    dept = models.ForeignKey ( Dept )
    
    vendor = models.ForeignKey ( Vendor )
    uniqueid = models.OneToOneField ( FinUniqueID , blank=True, null=True)

    def __unicode__ (self):
        return (self.creator.user.first_name + " " + self.creator.user.last_name + " " + unicode(self.id))

##VOUCHERS MODELS END##




##ADVANCE ALLOCATION MODELS##
class AdvanceRequest(models.Model):
    datecreated = models.DateField ( 'Date Created', auto_now_add = True )
    dateapproved = models.DateField ( 'Date Approved' , null=True, blank=True )
    amount = models.IntegerField ( default=0 )
    purpose = models.TextField ( null=True, blank=True )
    status = models.CharField ( max_length=1, choices = (( 'A', 'Approved' ),( 'P', 'Pending' )) )
    
    creator = models.ForeignKey ( ERPUser, related_name = 'advancerequest_created_set' )
    approver = models.ForeignKey ( ERPUser, related_name = 'advancerequest_approved_set'  , null=True, blank=True)
    subdept = models.ForeignKey ( Subdept, blank=True, null=True )
    dept = models.ForeignKey ( Dept )

    def __unicode__ (self):
        return (self.creator.user.first_name + " " + self.creator.user.last_name + " " + unicode(self.id)) 
##ADVANCE ALLOCATION MODELS END##





##PAYMENTS MODELS##
class PaymentRequest(models.Model):
    datecreated = models.DateField ( 'Date Created', auto_now_add = True )
    dateapproved = models.DateField ( 'Date Approved', null=True, blank=True )
    amount = models.IntegerField ( default=0 )
    purpose = models.TextField ( null=True, blank=True )
    status = models.CharField ( max_length=1, choices = (( 'A', 'Approved' ),( 'P', 'Pending' )) )
    
    creator = models.ForeignKey ( ERPUser, related_name = 'paymentrequest_created_set' )
    approver = models.ForeignKey ( ERPUser, related_name = 'paymentrequest_approved_set' , null=True, blank=True )
    subdept = models.ForeignKey ( Subdept, blank=True, null=True )
    dept = models.ForeignKey ( Dept )
    
    checknumber = models.TextField ( null=True, blank=True )
        
    def __unicode__ (self):
        return (self.creator.user.first_name + " " + self.creator.user.last_name + " " + unicode(self.id))
