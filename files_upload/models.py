from django.db import models
#from file_format import ContentTypeRestrictedFileField
from django.contrib.auth.models import User

class files_model(models.Model):
    title=models.CharField(max_length=100,help_text='(add a title to your image)')
    sponsor_type=models.CharField(max_length=100,choices=(('gen spons','gen spons'),('events_spons','events_spons')))
    events_sponsor=models.CharField(max_length=100,choices=(('fr','facilities and requirements'), ('robo','robotics')),help_text='(fill it only for the events sponsors)',blank=True)
    attachment=models.ImageField(upload_to='events/sponslogo/',help_text='(please keep file size below 5MB and give only imagess in jpg format)')
    user=models.ForeignKey(User)
    def __unicode__(self):
        return self.title
