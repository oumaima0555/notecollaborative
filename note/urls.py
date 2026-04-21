from django.urls import path
from .views import note_list, note_detail, note_create

urlpatterns = [
    path('', note_list, name='note_list'),
    path('create/', note_create, name='note_create'),
    path('<int:pk>/', note_detail, name='note_detail'),
]