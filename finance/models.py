from django.db import models
from users.models import ERPUser
from dept.models import Subdept, Dept

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
    dateapproved = models.DateField ( 'Date Approved' )
    amount = models.IntegerField ( default=0 )
    purpose = models.TextField ( null=True, blank=True )
    vendor = models.ForeignKey ( Vendor )
    creator = models.ForeignKey ( ERPUser, related_name = 'voucherrequest_created_set' )
    approver = models.ForeignKey ( ERPUser, null=True, blank=True, related_name = 'voucherrequest_approved_set' )
    status = models.CharField ( max_length=1, choices = (( 'A', 'Approved' ),( 'P', 'Pending' )) )
    subdept = models.ForeignKey ( Subdept, blank=True, null=True )
    dept = models.ForeignKey ( Dept )
    uniqueid = models.OneToOneField ( FinUniqueID )

    def __unicode__ (self):
        return unicode(self.id)

##VOUCHERS MODELS END##




##ADVANCE ALLOCATION MODELS##
class AdvanceRequest(models.Model):
    datecreated = models.DateField ( 'Date Created', auto_now_add = True )
    dateapproved = models.DateField ( 'Date Approved' )
    amount = models.IntegerField ( default=0 )
    purpose = models.TextField ( null=True, blank=True )
    creator = models.ForeignKey ( ERPUser, related_name = 'advancerequest_created_set' )
    approver = models.ForeignKey ( ERPUser, related_name = 'advancerequest_approved_set' )
    status = models.CharField ( max_length=1, choices = (( 'A', 'Approved' ),( 'P', 'Pending' )) )
    subdept = models.ForeignKey ( Subdept )

    def __unicode__ (self):
        return self.creator + ' ' + unicode(self.id)
 
##ADVANCE ALLOCATION MODELS END##





##PAYMENTS MODELS##
class PaymentRequest(models.Model):
    datecreated = models.DateField ( 'Date Created', auto_now_add = True )
    dateapproved = models.DateField ( 'Date Approved' )
    amount = models.IntegerField ( default=0 )
    purpose = models.TextField ( null=True, blank=True )
    checknumber = models.TextField ( null=True, blank=True )
    creator = models.ForeignKey ( ERPUser, related_name = 'paymentrequest_created_set' )
    approver = models.ForeignKey ( ERPUser, related_name = 'paymentrequest_approved_set' )
    status = models.CharField ( max_length=1, choices = (( 'A', 'Approved' ),( 'P', 'Pending' )) )
    subdept = models.ForeignKey ( Subdept )
        
    def __unicode__ (self):
        return self.creator + ' ' + unicode(self.id)
