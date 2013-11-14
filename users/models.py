 # ************* ERP - USERS APP - MODELS *************
from django.db import models
from django.contrib.auth.models import User
from dept.models import Dept, Subdept
from django.conf import settings
from events.models import GenericEvent
import datetime
from django.utils import timezone
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
    core_relations = models.ManyToManyField(Dept, null=True, blank=True, related_name='core_set')

    #Other information
    nickname = models.CharField(max_length=100, blank=True, null=True)
    chennai_number = models.CharField(max_length=15, blank=True, null=True)
    summer_number = models.CharField(max_length=15, blank=True, null=True)
    summer_stay = models.CharField(max_length=30, blank=True, null=True)
    hostel = models.CharField(max_length=15, choices = HOSTEL_CHOICES, blank=True, null=True)
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

BRANCH_CHOICES = (
    ('Arts', 'Arts'),
    ('Accounting', 'Accounting'),
    ('Applied Mechanics', 'Applied Mechanics'),
    ('Mechatronics', 'Mechatronics'),
    ('Aerospace Engineering', 'Aerospace Engineering'),
    ('Automobile Engineering', 'Automobile Engineering'),
    ('Biotech / Biochemical / Biomedical', 'Biotech / Biochemical / Biomedical'),
    ('Biology', 'Biology'),
    ('Ceramic Engineering', 'Ceramic Engineering'),
    ('Chemical Engineering', 'Chemical Engineering'),
    ('Chemistry', 'Chemistry'),
    ('Design', 'Design'),
    ('Engineering Design', 'Engineering Design'),
    ('Civil Engineering', 'Civil Engineering'),
    ('Computer Science and Engineering', 'Computer Science and Engineering'),
    ('Electronics and Communications Engineering', 'Electronics and Communications Engineering'),
    ('Electrical and Electronics Engineering', 'Electrical and Electronics Engineering'),
    ('Electrical Engineering', 'Electrical Engineering'),
    ('Electronics and Instrumentation Engineering', 'Electronics and Instrumentation Engineering'),
    ('Engineering Physics', 'Engineering Physics'),
    ('Economics', 'Economics'),
    ('Fashion Technology', 'Fashion Technology'),
    ('Humanities and Social Sciences', 'Humanities and Social Sciences'),
    ('Industrial Production', 'Industrial Production'),
    ('Production', 'Production'),
    ('Information Technology and Information Science', 'Information Technology and Sciences'),
    ('Management', 'Management'),
    ('Manufacturing', 'Manufacturing'),
    ('Mathematics', 'Mathematics'),
    ('Metallurgy and Material Science', 'Metallurgy and Material Science'),
    ('Mechanical Engineering', 'Mechanical Engineering'),
    ('Ocean Engineering and Naval Architecture', 'Ocean Engineering and Naval Architecture'),
    ('Physics', 'Physics'),
    ('Telecom', 'Telecom'),
    ('Textile Engineering', 'Textile Engineering'),
    ('Others', 'Others'),
)
GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

STATE_CHOICES = (
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu And Kashmir', 'Jammu And Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Orissa', 'Orissa'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman And Nicobar Islands', 'Andaman And Nicobar Islands'),
    ('Chandigarh', 'Chandigarh'),
    ('Dadra And Nagar Haveli', 'Dadra And Nagar Haveli'),
    ('Daman And Diu', 'Daman And Diu'),
    ('Lakshadweep', 'Lakshadweep'),
    ('NCT/Delhi', 'NCT/Delhi'),
    ('Puducherry', 'Puducherry'),
    ('Outside India', 'Outside India'),
)
class College(models.Model):

    name = models.CharField(max_length=255,
                            help_text='The name of your college. Please refrain from using short forms.'
                            )
    city = models.CharField(max_length=30,
                            help_text='The name of the city where your college is located. Please refrain from using short forms.'
                            )
    state = models.CharField(max_length=40, choices=STATE_CHOICES,
                             help_text='The state where your college is located. Select from the drop down list'
                             )
    def __unicode__(self):
        return '%s, %s, %s' % (self.name, self.city, self.state)

class UserProfile(models.Model):

    user               = models.ForeignKey(User, unique=True)
    gender             = models.CharField(max_length=1, choices=GENDER_CHOICES,
                              default='F')  # Defaults to 'girl' ;-)
    age                = models.IntegerField(default=18)
                              # help_text='You need to be over 12 and under 80 years of age to participate'
                              # No age limit now.
    branch             = models.CharField(max_length=50, choices=BRANCH_CHOICES,
                              help_text='Your branch of study')
    mobile_number      = models.CharField(max_length=15, blank=True, null=True,
                              help_text='Please enter your current mobile number')
    college            = models.ForeignKey(College, null=True, blank=True)
    college_roll       = models.CharField(max_length=40, null=True)

    shaastra_id        = models.CharField(max_length = 20, unique = True, null=True)

    activation_key     = models.CharField(max_length=40, null=True)
    key_expires        = models.DateTimeField(default = timezone.now()+datetime.timedelta(2))
    want_accomodation  = models.BooleanField(default=False, help_text = "Doesn't assure accommodation during Shaastra.")
    school_student    = models.BooleanField(default=False)
    is_core = models.BooleanField(default=False)
    is_hospi = models.BooleanField(default=False)

