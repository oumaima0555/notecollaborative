from django.shortcuts import render,redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Utilisateur,Administrateur,Collaborateur
from django.views import View


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authentifier l'utilisateur
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {user.email}!')
                return redirect('home')  # Rediriger vers la page d'accueil
            else:
                messages.error(request, 'Email ou mot de passe incorrect')
    else:
        form = LoginForm()
    
    return render(request, 'index.html', {'loginForm': form})

# Create your views here.
