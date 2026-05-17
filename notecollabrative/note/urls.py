from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_liste, name='note_liste'),
    path('recherche/', views.recherche_notes, name='recherche_notes'),
    path('<int:note_id>/export/markdown/', views.exporter_markdown, name='exporter_markdown'),
    path('<int:note_id>/export/pdf/', views.exporter_pdf, name='exporter_pdf'),
    path('ajouter/', views.note_ajouter, name='note_ajouter'),
    path('<int:id>/', views.note_detail, name='note_detail'),
    path('<int:id>/modifier/', views.note_modifier, name='note_modifier'),
    path('<int:id>/supprimer/', views.note_supprimer, name='note_supprimer'),

    path('<int:note_id>/version/', views.version, name='version'),
    path('<int:note_id>/medias/', views.media_liste, name='media_liste'),
    path('<int:note_id>/media/ajouter/', views.media_ajouter, name='media_ajouter'),
    path('media/<int:media_id>/supprimer/', views.media_supprimer, name='media_supprimer'),
    path('notes/<int:note_id>/partager/', views.partage_ajouter, name='partage_ajouter'),
    path('partage/<int:partage_id>/modifier/', views.partage_modifier, name='partage_modifier'),
    path('partage/<int:partage_id>/supprimer/', views.partage_supprimer, name='partage_supprimer'),
    path('categories/', views.categorie_liste, name='categorie_liste'),
    path('categories/ajouter/', views.categorie_ajouter, name='categorie_ajouter'),
    path('categories/<int:id>/modifier/', views.categorie_modifier, name='categorie_modifier'),
    path('categories/<int:id>/supprimer/', views.categorie_supprimer, name='categorie_supprimer'),
    path('collaborations/', views.collaborations_avec_moi, name='collaborations_avec_moi'),
]