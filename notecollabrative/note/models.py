from django.db import models
from django.utils import timezone
from django.conf import settings


class Categorie(models.Model):
    nom = models.CharField(max_length=50, default='categorie')
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.nom


class Note(models.Model):
    contenu = models.TextField(blank=True, default='')
    titre = models.CharField(max_length=50, default='sans titre')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    tags = models.ManyToManyField(
    'tag.Tag',
    through='tag.note_tag',
    blank=True,
    related_name='notes'
   )

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.titre

class Partage(models.Model):
    PERMISSIONS = [
        ('lecture', 'Lecture'),
        ('commentaire', 'Commentaire'),
        ('edition', 'Édition'),
    ]

    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='partages'
    )

    collaborateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes_partagees'
    )

    permission = models.CharField(
        max_length=20,
        choices=PERMISSIONS,
        default='lecture'
    )

    date_partage = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.note.titre} - {self.collaborateur} - {self.permission}"


class Version(models.Model):
    contenu = models.TextField(blank=True, default='')
    date_modification = models.DateTimeField(auto_now=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='versions')

    def __str__(self):
        return self.contenu[:50]


class Media(models.Model):
    TYPES = [
        ('lien', 'Lien'),
        ('image', 'Image'),
    ]

    type = models.CharField(max_length=50, choices=TYPES, default='lien')
    url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='medias/images/', blank=True, null=True)
    date_upload = models.DateTimeField(default=timezone.now)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='medias')
    
    est_interne = models.BooleanField(default=False)

    def __str__(self):
        if self.url:
            return self.url
        if self.image:
            return self.image.name
        return self.type