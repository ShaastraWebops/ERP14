from django.db import models
#from file_format import ContentTypeRestrictedFileField
from django.contrib.auth.models import User

class files_model(models.Model):
    title=models.CharField(max_length=100,help_text='(Add a title to your image)')
    sponsor_type=models.CharField(max_length=100,choices=(('gen spons','Gen Spons'),('events_spons','Events Spons')))
    events_sponsor=models.CharField(max_length=100,choices=(('fr','Facilities and Requirements'), ('robo','Robotics')),help_text='(Fill it only for the events sponsors)',blank=True)
    attachment=models.ImageField(upload_to='events/sponslogo/',help_text='(Please keep file size below 5MB and give only imagess in jpg format)')
    user=models.ForeignKey(User)
    def __unicode__(self):
        return self.title
