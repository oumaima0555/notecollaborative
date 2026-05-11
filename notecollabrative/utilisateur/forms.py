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

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'entrer password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'confirmer password'
        })
    )

    def clean(self):

        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'les mots de passe ne correspondent pas')
        return cleaned_data

    class Meta:

        model = Collaborateur

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]