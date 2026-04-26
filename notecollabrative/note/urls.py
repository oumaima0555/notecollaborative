from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_liste, name='note_liste'),
    path('<int:id>/', views.note_detail, name='note_detail'),
    path('<int:note_id>/version/', views.version, name='version'),
]