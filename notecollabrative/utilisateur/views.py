from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User

from .forms import RegisterForm
from .models import Utilisateur, Administrateur, Collaborateur


@login_required(login_url='login')
def home(request):

    return render(
        request,
        'home.html'
    )


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = None

        # connexion avec username
        user = authenticate(
            request,
            username=username,
            password=password
        )

        # connexion avec email
        if user is None:

            try:

                user_obj = Utilisateur.objects.get(email=username)

                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password
                )

            except Utilisateur.DoesNotExist:
                pass

        if user is not None:

            login(request, user)

            messages.success(
                request,
                'Connexion réussie'
            )

            return redirect('home')

        else:

            messages.error(
                request,
                'Nom utilisateur ou mot de passe incorrect'
            )

    return render(
        request,
        'login.html'
    )


def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password= form.cleaned_data.get('password')
            user = Utilisateur.objects.create_user(username=username,email=email, password=password)
            login(request, user)
            messages.success(
                request,
                'Compte créé avec succès'
            )
            return redirect('home') 
    
        else:
            print(form.errors)
            messages.error(
                request,
                'Erreur dans le formulaire'
            )

    else:

        form = RegisterForm()

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )


def logout_view(request):

    logout(request)

    messages.success(
        request,
        'Déconnexion réussie'
    )

    return redirect('login')


@login_required
def profile_view(request):

    if request.method == 'POST':

        user = request.user

        user.username = request.POST.get('username')
        user.email = request.POST.get('email')

        password = request.POST.get('password')

        if password:
            user.set_password(password)

        user.save()

        # باش يبقى connecté
        login(request, user)

        messages.success(
            request,
            'Profil modifié avec succès'
        )

        return redirect('profile')

    return render(
        request,
        'profile.html'
    )