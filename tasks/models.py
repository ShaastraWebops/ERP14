# ********* ERP - TASKS APP - MODELS ***********

from django.db import models
from users.models import ERPUser
from dept.models import Subdept, Dept
from django.contrib.auth.models import User

from datetime import date

TASK_STATUSES = (  
        ( 'U' , 'UNAPPROVED' ) ,
        ( 'O' , 'APPROVED AND ONGOING' ) ,
        ( 'A' , 'APPROVED, ALMOST DONE' ) ,
        ( 'R' , 'REPORTED COMPLETED' ) ,
        ( 'C' , 'COMPLETED' ) ,
    )

class Task(models.Model):
    
    #Central task information
    taskcreator = models.ForeignKey(ERPUser, related_name='created_task_set')
    datecreated = models.DateField ('Date Created', auto_now_add = True )
    datelastmodified = models.DateField ('Date Last Modified',  auto_now = True ) #auto_now will give us the last modified date.
    deadline = models.DateField ('Deadline')
    
    #Description of the task
    subject = models.CharField (max_length=100)
    #TODO : FORMATTING CAPABLITY?
    description = models.TextField ( null = True, blank = True )
    
    #Group of users doing the task.
    taskforce = models.ManyToManyField (ERPUser, related_name='task_set')
    
    #The related-names above and below are the default values. I've left them in for easy modification.
    
    #Classify tasks by subdepartments to facilitate easy querying.
    targetsubdepts = models.ManyToManyField (Subdept, related_name='task_set')
    
    #Taking care of cross-departmental tasks.
    origindept = models.ForeignKey(Dept, related_name='created_task_set')
    targetdept = models.ForeignKey(Dept, related_name='todo_task_set')
    isxdepartmental = models.BooleanField(default=False, blank=True)
    
    #This is the task status variable.
    #One question is what it defaults to. This depends on isxdepartmental.
    #TODO: Write a method that handles this.
#SAMIR: The default could be unapproved. In case of a intradepartmental task created by a core, the view will take care of automatically approving it.
    taskstatus = models.CharField ( max_length=1, choices=TASK_STATUSES )

    #Task Nesting
    parenttask = models.ForeignKey('self', null=True, blank=True, default=None, related_name='childtask_set')
    depthlevel = models.IntegerField(default=0, blank=True)

    def __unicode__(self):
        return self.description

    def isPastDeadline():
        return date.today() > self.Deadline
        
    #Overriding the default save function
    def save(self, *args, **kwargs):

        super(Task, self).save(*args, **kwargs) 
        # Set the depth level of the task
        if self.parenttask == None:
            self.depthlevel = 0
        else:
            self.depthlevel = self.parenttask.depthlevel + 1
        
        #Set if it's cross departmental or not.
        if self.origindept == self.targetdept:
            self.isxdepartmental = False
        else:
            self.isxdepartmental = True
            
        #Set the target subdepartments, if a taskforce has been assigned
        if self.taskforce.count():    
            #Empty targetsubdepts
            self.targetsubdepts.clear()

            #Fill targetsubdepts with concerned subdepartments of the TaskForce
            if self.targetdept:
                for user in self.taskforce.all():
                    for usersubdept in user.coord_relations.all():
                        if usersubdept.dept == self.targetdept:
                            self.targetsubdepts.add(usersubdept)
            
        
        # Call the "real" save() method.
        super(Task, self).save(*args, **kwargs) 
        #do_something_else()
    
                        
    #Helps check if the origin core is allowed to edit the cross departmental task.
    def isUnapprovedCrosstask(self):
        if ((self.isxdepartmental == True) and (self.taskstatus == 'U')):
            return True
        else:
            return False
            
class Comment (models.Model):
    """
    Comments Class to store a comment related to a task.

    Timestamp helps to order comments. It is generated automatically.
    Author can be used to select particular comments based on the author.
    """
    author = models.ForeignKey (User)
    task = models.ForeignKey (Task)
    comment_string = models.TextField ()
    time_stamp = models.DateTimeField (auto_now = True, editable = False)

    class Meta:
        ordering = ['time_stamp']
    
    def __str__(self):
        return '%s %s' %(self.task.subject, self.id)
    class Admin:
        pass

