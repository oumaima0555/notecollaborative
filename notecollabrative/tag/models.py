from django.db import models
from note.models import Not
# Create your models here.

class Tag(models.Model):
    id_tag=models.BigAutoField(primary_key=True)
    nom_tag=models.CharField(max_length=255,null=False)

    def __str__(self):
        return self.nom_tag
    

class note_tag(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['note', 'tag']  # Empêche les doublons
    
    def lierTag(self):
        """Lier un tag à une note"""
        self.save()
    
    def delierTag(self):
        """Délier un tag d'une note"""
        self.delete()
    
    def __str__(self):
        return f"{self.note.titre} - {self.tag.nom_tag}"