 # ************* ERP - USERS APP - MODELS *************
from django.db import models
from django.contrib.auth.models import User
from dept.models import Dept, Subdept
from django.conf import settings

# Create your models here.


#Annoying little details
HOSTEL_CHOICES  =(
                  ("Ganga", "Ganga"),
                  ("Mandak", "Mandak"),
                  ("Jamuna", "Jamuna"),
                  ("Alak", "Alak"),
                  ("Saraswathi", "Saraswathi"),
                  ("Narmada", "Narmada"),
                  ("Godav", "Godav"),
                  ("Pampa", "Pampa"),
                  ("Tambi", "Tambi"),
                  ("Sindhu", "Sindhu"),
                  ("Mahanadi", "Mahanadi"),
                  ("Sharavati", "Sharavati"),
                  ("Krishna", "Krishna"),
                  ("Cauvery", "Cauvery"),
                  ("Tapti", "Tapti"),
                  ("Brahmaputra", "Brahmaputra"),
                  ("Sarayu", "Sarayu"),
                  )


#User Profile Model
class ERPUser(models.Model):
    user = models.OneToOneField(User)
    dept = models.ForeignKey(Dept, related_name='dept_user_set')
    subdept = models.ForeignKey(Subdept, blank=True, null=True, default=None, related_name='subdept_user_set')
    status = models.IntegerField (default=0) # 0 = Coord, 1 = Supercoord, 2 = Core
    
    #Handling the Multiple Identity Problem
    multiple_ids = models.BooleanField(default=False)
    coord_relations = models.ManyToManyField(Subdept, null=True, blank=True, related_name='coord_set')
    supercoord_relations = models.ManyToManyField(Dept, null=True, blank=True, related_name='supercoord_set')
    core_relations = models.ForeignKey(Dept, null=True, blank=True, related_name='core_set')

    #Other information
    nickname = models.CharField(max_length=30, blank=True)
    chennai_number = models.CharField(max_length=15, blank=True)
    summer_number = models.CharField(max_length=15, blank=True)
    summer_stay = models.CharField(max_length=30, blank=True)
    hostel = models.CharField(max_length=15, choices = HOSTEL_CHOICES, blank=True)
    room_no = models.IntegerField(default=0, blank=True, null=True )

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name
    
    # Methods to check if user is core/supercoord/coord
    def is_coord(self):
        return self.status == 0
    
    def is_supercoord(self):
        return self.status == 1
    
    def is_core(self):
        return self.status == 2
        
        
class UserPhoto(models.Model):
    user = models.ForeignKey(ERPUser)
    photo_path = models.FileField(upload_to=settings.MEDIA_ROOT)

    def __str__(self):
        return str(self.photo_path)
    class Admin:
        pass
