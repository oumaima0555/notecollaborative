from django.urls import path
from . import views

app_name = 'tags'

urlpatterns = [

    path('', views.liste_tags, name='liste_tags'),

    path('ajouter/', views.ajouter_tag, name='ajouter_tag'),

    path('modifier/<int:id>/', views.modifier_tag, name='modifier_tag'),

    path('supprimer/<int:id>/', views.supprimer_tag, name='supprimer_tag'),
]