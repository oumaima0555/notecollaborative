
from django.urls import path
from . import views

urlpatterns = [

    # LOGIN
    path('', views.login_view, name='login'),

    path('login/', views.login_view, name='login'),

    # HOME
    path('home/', views.home, name='home'),

    # REGISTER
    path('register/', views.register_view, name='register'),

    # LOGOUT
    path('logout/', views.logout_view, name='logout'),

    # PROFILE
    path('profile/', views.profile_view, name='profile'),

]