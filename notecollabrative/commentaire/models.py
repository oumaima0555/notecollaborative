from django.db import models
from django.utils import timezone

class Commentaire(models.Model):

    id_contenu = models.BigAutoField(primary_key=True)

    contenu_com = models.TextField(
        blank=True,
        default=''
    )

    date_com = models.DateField(
        default=timezone.now,
        null=True,
        blank=True
    )

    utilisateur = models.ForeignKey(
        'utilisateur.Utilisateur',
        on_delete=models.CASCADE,
        related_name='commentaires',
        null=True,
        blank=True
    )

    note = models.ForeignKey(
        'note.Note',
        on_delete=models.CASCADE,
        related_name='commentaires',
        null=True,
        blank=True
    )

    # Modifier commentaire
    def set_commentaire(self, contenu_com):
        self.contenu_com = contenu_com
        self.save()

    def __str__(self):
        return f"Commentaire de {self.utilisateur} le {self.date_com}"