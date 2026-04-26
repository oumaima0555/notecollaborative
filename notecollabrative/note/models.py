from django.db import models
from django.utils import timezone

date_upload = models.DateTimeField(default=timezone.now)

# Create your models here.
class Categorie(models.Model):
    nom=models.CharField(max_length=50,default='categorie')
    description=models.TextField(blank=True, default='')
    def __str__(self):
        return self.nom

class Note(models.Model):
    contenu=models.TextField(blank=True, default='')
    titre=models.CharField(max_length=50,default='sans titre')
    date_creation=models.DateTimeField(auto_now_add=True)
    date_modification=models.DateTimeField(auto_now=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True,blank=True)
    def __str__(self):
        return self.titre

class Partage(models.Model):
    permission=models.CharField(max_length=50,default='')
    note = models.ForeignKey( Note, on_delete=models.CASCADE,related_name='partages')
    def __str__(self):        return self.permission

class Version(models.Model):
    contenu=models.TextField(blank=True, default='')
    date_modification=models.DateTimeField(auto_now=True)
    note = models.ForeignKey(Note,on_delete=models.CASCADE,related_name='versions'
    )
    def __str__(self):        return self.contenu[:50]

class Media(models.Model):
    type=models.CharField(max_length=50,default='')
    url=models.URLField(default='')
    date_upload=models.DateTimeField(default=timezone.now)
    note = models.ForeignKey(Note,on_delete=models.CASCADE,related_name='medias'
    )
    def __str__(self):
        return self.url[:50]
   
   
