from django.db import models
from django.utils import timezone

# Create your models here.
class Commentaire(models.Model):

    id_contenu=models.BigAutoField(primary_key=True)
    contenu_com=models.TextField(blank=True, default='')
    date_com=models.DateField(default=timezone.now, null=True, blank=True)
    utilisateur=models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, related_name='commentaires', null=True, blank=True)
    
    # la fonction d'ajouter commentaire
    def __init__(self, utilisateur,contenu_com):
        super().__init__()
        self.utilisateur = utilisateur;
        self.contenu_com = contenu_com;

    def set_commentaire(self, contenu_com):
        self.contenu_com = contenu_com

    def __str__(self):
        return f"Commentaire de {self.utilisateur} le {self.date_com}"
    


     