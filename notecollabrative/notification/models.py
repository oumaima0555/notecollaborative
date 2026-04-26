from django.db import models
from django.utils import timezone

# Create your models here.
class Notification(models.Model):

    id_notification=models.AutoField(primary_key=True)
    messsage=models.CharField(max_length=255, blank=True, default='')
    date=models.DateTimeField(default=timezone.now, null=True, blank=True)
    lu=models.BooleanField(default=False)
    utilisateur=models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    def envoyer_notification(self,utilisateur,message):
        notification=Notification(messsage=message)
        notification.save()
        # Logique pour envoyer la notification à l'utilisateur
    def marque_lue(self):
        self.lu=True
        self.save()    
    def __str__(self):
        return self.messsage

