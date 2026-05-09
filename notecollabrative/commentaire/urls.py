from django.urls import path
from . import views

app_name = 'Commentaire'

urlpatterns = [

    path(
        'ajouter/<int:note_id>/',
        views.ajouter_commentaire,
        name='ajouter_commentaire'
    ),
]