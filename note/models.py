from django.db import models


class Tag(models.Model):
    nom_tag = models.CharField(max_length=100)

    def __str__(self):
        return self.nom_tag


class Note(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.titre


class Media(models.Model):
    TYPE_CHOICES = [
        ('image', 'Image'),
        ('lien', 'Lien'),
        ('fichier', 'Fichier'),
    ]

    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='medias')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    url = models.URLField(blank=True, null=True)
    fichier = models.FileField(upload_to='medias/', blank=True, null=True)
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.note.titre}"