from django.db import models
from utilisateur.models import Utilisateur
# Create your models here.
class Commentaire(models.Model):

    id_contenu=models.BigAutoField(primary_key=True)
    contenu_com=models.TextField()
    date_com=models.DateField(auto_now_add=True)
    utilisateur=models.ForeignKey(Utilisateur,on_delete=models.CASCADE,related_name='commentaires')
    
    # la fonction d'ajouter commentaire
    def __init__(self, utilisateur,contenu_com):
        super().__init__()
        self.utilisateur = utilisateur;
        self.contenu_com = contenu_com;

    def set_commentaire(self, contenu_com):
        self.contenu_com = contenu_com

    def __str__(self):
        return f"Commentaire de {self.utilisateur} le {self.date_com}"
    


     