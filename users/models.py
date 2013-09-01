 # ************* ERP - USERS APP - MODELS *************
from django.db import models
from django.contrib.auth.models import User
from dept.models import Dept, Subdept
from django.conf import settings
from events.models import GenericEvent
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
    
    #THIS SET OF ATTRIBUTES REPRESENTS THE CURRENTLY SELECTED PROFILE OF THE USER.
    
    user = models.OneToOneField(User) # The corresponding auth user
    dept = models.ForeignKey(Dept, related_name='dept_user_set') # The department in which the user is
    subdept = models.ForeignKey(Subdept, blank=True, null=True, default=None, related_name='subdept_user_set') # The subdept of the user (used in 
    status = models.IntegerField (default=0) # 0 = Coord, 1 = Supercoord, 2 = Core
    event = models.ForeignKey(GenericEvent, null=True, blank=True)    

    #THIS SET OF ATTRIBUTES STORES THE VARIOUS IDENTITIES OF THE USER.
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
        
    def get_position (self):
        if self.status == 2:
            return 'Core'
        if self.status == 1:
            return 'Supercoord'
        if self.status == 0:
            return 'Coord'
            
    def get_dept_subdept(self):
        dept_str = self.dept.name
        if self.subdept:
            dept_str += " (" + self.subdept.name + ")"
        return dept_str

        
class UserPhoto(models.Model):
    user = models.ForeignKey(ERPUser)
    photo_path = models.FileField(upload_to=settings.MEDIA_ROOT)

    def __str__(self):
        return str(self.photo_path)
    class Admin:
        pass
