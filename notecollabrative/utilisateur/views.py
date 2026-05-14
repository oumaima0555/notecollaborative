from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

User = get_user_model()
# LOGIN
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # admin ممنوع من login normal
            if user.is_superuser:

                return render(request, 'login.html', {
                    'error': 'Admin doit se connecter depuis /admin'
                })

            login(request, user)

            return redirect('home')

        else:

            return render(request, 'login.html', {
                'error': 'Username ou password incorrect'
            })

    return render(request, 'login.html')

def register_view(request):

    if request.method == "POST":

        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        num = request.POST.get("num")

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():

            return render(request, 'register.html', {
                'error': 'Username déjà existe'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            nom=nom,
            prenom=prenom,
            num=num
        )

        login(request, user)

        return redirect('home')

    return render(request, 'register.html')
# HOME
def dashboard(request):

    return render(request, 'home.html')


# PROFILE
def profile_view(request):

    return render(request, 'profile.html')


# LOGOUT
def logout_view(request):

    logout(request)

    return redirect('login')