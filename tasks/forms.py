from django import forms
from django.forms import ModelForm, Select
from tasks.models import Task
from users.models import ERPUser
from dept.models import Subdept


# _____________--- INTRADEPARTMENTAL TASK FORM ---______________#
class IntraTaskForm(ModelForm):
    #Temporary solution to provide options for selecting a taskforce.
    coords = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset = ERPUser.objects.none(), required=False)
    supercoords = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset = ERPUser.objects.none(), required=False )
    cores = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset = ERPUser.objects.none(), required=False)
    
    class Meta:
        model = Task
        fields = ['deadline', 'subject', 'description']
        widgets = {
            'deadline': forms.DateInput(format='%Y-%m-%d'),
        }
    
    def clean(self):
        cleaned_data = super(IntraTaskForm, self).clean()
        cores = self.cleaned_data['cores']
        coords = self.cleaned_data['coords']
        supercoords = self.cleaned_data['supercoords']
        
        if ((not cores) and (not coords) and (not supercoords)):
            raise forms.ValidationError("The Task Force cannot be empty.")
                
        return cleaned_data
            
    #Framework for getting a QuerySet of Coords, Supercoords, and Cores.
    def __init__(self, department, *args, **kwargs):
        super (IntraTaskForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['coords'].queryset = ERPUser.objects.filter(coord_relations__dept=department)
        self.fields['supercoords'].queryset = department.supercoord_set.all()
        self.fields['cores'].queryset = department.core_set.all()
        
        # Below code is to put the current taskforce into the form if "instance" kwarg is used.
        instance = kwargs.pop('instance', None)
        
        if instance is not None:
            print instance.taskforce.all()
            for user_temp in instance.taskforce.all():
                print user_temp.dept, user_temp.status
                if user_temp.dept == department and user_temp.status == 0 \
                        and user_temp in self.fields['coords'].queryset: #Coord in the department
                    if self.fields['coords'].initial == None:
                        self.fields['coords'].initial = [user_temp]
                    else:
                        self.fields['coords'].initial.append(user_temp) 
                elif user_temp.dept == department and user_temp.status == 1 \
                        and user_temp in self.fields['supercoords'].queryset: #SuperCoord in the department
                    if self.fields['supercoords'].initial == None:
                        self.fields['supercoords'].initial = [user_temp]
                    else:
                        self.fields['supercoords'].initial.append(user_temp) 
                elif user_temp.dept == department and user_temp.status == 2 \
                        and user_temp in self.fields['cores'].queryset: #Cores in the department
                    if self.fields['cores'].initial == None:
                        self.fields['cores'].initial = [user_temp]
                    else:
                        self.fields['cores'].initial.append(user_temp) 
        else:
            print "No instance passed."
        
# _____________--- CROSSDEPARTMENTAL TASK FORM ---______________#
class CrossTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['deadline', 'subject', 'description', 'targetsubdepts']
        widgets = {
            'targetsubdepts': forms.CheckboxSelectMultiple,
            'deadline': forms.DateInput(format='%Y-%m-%d'),
        }
        
    def clean_targetsubdepts(self):
        value = self.cleaned_data['targetsubdepts']
        if (len(value) > 1) or (len(value) == 0):
            raise forms.ValidationError("Select one and only one foreign subdepartment to assign the task to.")
        return value
    
    #Framework for getting a QuerySet of Subdepartments.
    def __init__(self, department, *args, **kwargs):
        super (CrossTaskForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['targetsubdepts'].queryset = Subdept.objects.exclude(dept=department)
        
