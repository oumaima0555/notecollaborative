from django.db import models

from django.contrib.auth.models import AbstractUser,Group,Permission    
#voici les models 

class Utilisateur(AbstractUser):
    id=models.AutoField(primary_key=True)
    nom=models.CharField(max_length=100)
    prenom=models.CharField(max_length=100)
    num=models.CharField(max_length=20)
    date_inscription=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    groups=models.ManyToManyField(
        Group, 
        related_name='utilisateurs',
        related_query_name='utilisateur',
        blank=True,
        help_text='the groups this user belongs to. A user will get all permissions granted to each of their groups.'
        )
    user_permissions=models.ManyToManyField(
        Permission,
        related_name='utilisateurs',
        related_query_name='utilisateur',
        blank=True,
        help_text='specific permissions for this user.'
        )
    
    def add_commentaire(self, contenu_com):
        from commentaire.models import Commentaire
        Commentaire.__init__(self, self, contenu_com)

    def modifier_commentaire(self, commentaire, nouveau_contenu):
        commentaire.set_commentaire(nouveau_contenu)

    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
class Administrateur(Utilisateur):
    # Ajoutez des champs spécifiques à l'administrateur si nécessaire
    def supprimer_utilisateur(self,utilisateur):
        utilisateur.delete()

    def modifier_utilisateur(self,utilisateur):
        # Implémentez la logique pour modifier les informations de l'utilisateur
        pass

class Collaborateur(Utilisateur):
    # Ajoutez des champs spécifiques au collaborateur si nécessaire
    def __str__(self):
        return super().__str__()
    