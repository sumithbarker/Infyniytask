from django.forms import ModelForm
from django import forms
from app.models import TODO,User,Employee
class TODOForm(ModelForm):
    class Meta:
        model = TODO
        fields = ['title' , 'status' , 'priority','assigned_to']#


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    class Meta:
        model = Employee
        fields = ["username","password","email","full_name","address"]


    def clean_username(self):
        uname = self.cleaned_data.get('username')
        if User.objects.filter(username = uname).exists():
            raise forms.ValidationError("Username already exists")

        return uname
    
# class UserLoginForm(AuthenticationForm):
    #class Meta:
        #model = User  # Assuming 'User' is your user model
        #fields = ['username', 'password']
        

class AdminlLoginForm(forms.ModelForm):
    class Meta:
        model = User # Associate the form with the Task model
        fields = ['username','password']

class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class AdminHomeForm(forms.ModelForm):
    class Meta:
        model = TODO  # Associate the form with the Task model
        fields = ['title', 'status', 'priority','assigned_to']



        

class TODOForm(ModelForm):
    class Meta:
        model = TODO
        fields = ['title', 'status', 'priority','assigned_to']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TODOForm, self).__init__(*args, **kwargs)
        if self.user:
            # Restrict queryset for assigned_to to only the current user
            employee = Employee.objects.get(user=self.user)
            self.fields['assigned_to'].queryset = Employee.objects.filter(pk=employee.pk)





# class EditUserProfileForm(UserChangeForm):
#     password= None
#     class Meta:
#         model= TODO
#         fields=['title' , 'status' , 'priority']
#         labels= {'email':'Email'}


# class EditAdminProfileForm(UserChangeForm):
#     password= None
#     class Meta:
#         model= TODO
#         fields=['title' , 'status' , 'priority','assigned_to']
#         labels= {'email':'Email'}