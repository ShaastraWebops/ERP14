from django.db import models
#from file_format import ContentTypeRestrictedFileField
from django.contrib.auth.models import User

class files_model(models.Model):
    title=models.CharField(max_length=100,help_text='(Add a title to your image)')
    sponsor=models.CharField(max_length=100,choices=(('gen spons','Gen Spons'),('Events Spons',(('fr','FR'),('robo','Robo')))))
    attachment=models.ImageField(upload_to='varun/',help_text='(Please keep file size below 5MB and give only images in jpg format)')
    #user=models.OneToOneField(User)uncomment this after implementing login
