from django.db import models

from django.contrib.auth.models import AbstractUser,Group,Permission    

#voici les models 

class Utilisateur(AbstractUser):
    # Ajoutez des champs personnalisés si nécessaire
    pass

class Administrateur(Utilisateur):
    # Ajoutez des champs spécifiques à l'administrateur si nécessaire
    pass

class Collaborateur(Utilisateur):
    # Ajoutez des champs spécifiques au collaborateur si nécessaire
    pass