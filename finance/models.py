from django.db import models
from users.models import ERPUser
from dept.models import Subdept

##VOUCHERS MODELS####
class Vendor(models.Model):
    
    name = models.CharField ( max_length=30 )

class FinUniqueID(models.Model):
    
    value = models.CharField ( max_length=30 )
    vendor = models.ForeignKey ( Vendor )

class VoucherRequest(models.Model):

    datecreated = models.DateField ( 'Date Created', auto_now_add = True )
    dateapproved = models.DateField ( 'Date Approved' )
    amount = models.IntegerField ( default=0 )
    purpose = models.TextField ( null=True, blank=True )
    vendor = models.ForeignKey ( Vendor )
    creator = models.ForeignKey ( ERPUser, related_name = 'voucherrequest_created_set' )
    approver = models.ForeignKey ( ERPUser, related_name = 'voucherrequest_approved_set' )
    status = models.CharField ( max_length=1, choices = (( 'A', 'Approved' ),( 'P', 'Pending' )) )
    subdept = models.ForeignKey ( Subdept )
    uniqueid = models.OneToOneField ( FinUniqueID )

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
 
##ADVANCE ALLOCATION MODELS END##

##PAYMENTS MODELS##

