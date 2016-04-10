from django import forms
from django.forms import widgets
from .models import Vacation, CustomUserModel
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import dateutil.parser


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUserModel
        fields = ('email', 'password','confirmpassword',)
        widgets = {
        'password': forms.PasswordInput(),
        'confirmpassword': forms.PasswordInput(),}

    def clean(self):
        username = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(u'Username "%s" is already in use.' % username)

        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirmpassword')

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data
    
class CustomLoginForm(forms.Form):
    email = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)
    widgets = {
        'password': forms.PasswordInput(),
        }
    def clean(self):
        username = self.cleaned_data['email']
        password = self.cleaned_data['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")                    
            else:
                print("The password is valid, but the account has been disabled!")
                raise forms.ValidationError("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
            raise forms.ValidationError("The username and password were incorrect.")

        return self.cleaned_data
    
class VacationForm(forms.ModelForm):
    class Meta:
        model = Vacation
        fields = ('description', 'from_date', 'to_date',)

        widgets = {'from_date': forms.DateInput(attrs={'class': 'datepicker'})}
        widgets = {'to_date': forms.DateInput(attrs={'class': 'datepicker'})}


                   
