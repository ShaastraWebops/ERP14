# ************ ERP - DEPTARMENTS APP - MODELS *****************
from django.db import models

# Create your models here.

#Department Model
class Dept(models.Model):
    name = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.name	


class Subdept(models.Model):
    name = models.CharField(max_length=30)
    dept = models.ForeignKey(Dept)

    def __unicode__(self):
        return self.name
