from django import forms
from .models import Administrateur, Collaborateur


class LoginForm(forms.ModelForm):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input',
            'placeholder': 'entrer email'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'entrer password'
        })
    )

    class Meta:
        model = Administrateur
        fields = ['email', 'password']


# ==========================
# FORMULAIRE INSCRIPTION
# ==========================

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'entrer password'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'confirmer password'
        }))

    class Meta:

        model = Collaborateur

        fields = [
            'username',
            'email',
            
            'password',
            'password1'
        ]

        def clean(self):
            
            cleaned_data = super().clean()

            password = cleaned_data.get('password')
            password1 = cleaned_data.get('password1')

            if password and password1 and password != password1:
                raise forms.ValidationError(
                    'Les mots de passe ne correspondent pas.'
                )
            
            return cleaned_data