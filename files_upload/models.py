from django.db import models
#from file_format import ContentTypeRestrictedFileField
from django.contrib.auth.models import User

class files_model(models.Model):
    title=models.CharField(max_length=100,help_text='(add a title to your image)')
    sponsor=models.CharField(max_length=100,choices=(('gen spons','gen spons'),('events spons',(('fr','fr'),('robo','robo')))))
    attachment=models.ImageField(upload_to='varun/',help_text='(please keep file size below 5MB and give only imagess in jpg format)')
    #user=models.OneToOneField(User)uncomment this after implementing login
