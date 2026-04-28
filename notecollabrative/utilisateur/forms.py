from django import forms
from .models import Administrateur,Collaborateur

class LoginForm(forms.ModelForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'input',
        'placeholder':'entrer email'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'input',
        'placeholder':'entrer password'
    }))

    class Meta:
        model=Administrateur
        fields= ['email','password']