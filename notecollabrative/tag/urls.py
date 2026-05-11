from django.urls import path
from . import views

urlpatterns = [

    path('', views.liste_tags, name='liste_tags'),

    path('ajouter/', views.ajouter_tag, name='tag_ajouter'),

    path('modifier/<int:id_tag>/', views.modifier_tag, name='tag_modifier'),

    path('supprimer/<int:id_tag>/', views.supprimer_tag, name='tag_supprimer'),

]