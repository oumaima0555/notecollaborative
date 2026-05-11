from django.urls import path
from . import views

urlpatterns = [

    path(
        'ajouter/<int:note_id>/',
        views.ajouter_commentaire,
        name='ajouter_commentaire'
    ),

    path(
        'modifier/<int:id>/',
        views.modifier_commentaire,
        name='commentaire_modifier'
    ),

    path(
        'supprimer/<int:id>/',
        views.supprimer_commentaire,
        name='commentaire_supprimer'
    ),

]