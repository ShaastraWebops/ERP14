from django import forms
from users.models import ERPUser
from dept.models import Dept, Subdept



class ChooseIdentityForm(forms.Form):

    coordships = forms.ModelChoiceField( queryset = Subdept.objects.none(), required=False)#, help_text = 'Choose a coordship' )
    supercoordships = forms.ModelChoiceField( queryset = Dept.objects.none(), required=False)#, help_text = 'Choose a supercoordship' )

    #Framework for getting a QuerySet of Coordships and Supercoordships
    def __init__(self, curruser, *args, **kwargs):
        super (ChooseIdentityForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['coordships'].queryset = curruser.coord_relations.all() 
        self.fields['supercoordships'].queryset = curruser.supercoord_relations.all()
 
class EditProfileForm (forms.ModelForm):
    class Meta:
        model = ERPUser 
        fields = ('nickname','chennai_number', 'summer_number', 'summer_stay', 'hostel', 'room_no',)

    def clean_chennai_number(self):
        number1 = self.cleaned_data['chennai_number']
        print len(number1)
        try:
            int(number1)
        except ValueError, e:
            raise forms.ValidationError ("Enter a valid number")
        if number1 == '':
            return number1
        elif ((len(number1)<9) or (len(number1)>12)):
            raise forms.ValidationError ("Enter a valid number")
        else :
            return self.data['chennai_number']
    
    def clean_room_no(self): # To avoid - "NULL cannot be saved" error
        rno = self.cleaned_data.get('room_no')
        if rno is None:
            return 0
        else:
            return rno

    class Admin:
        pass
