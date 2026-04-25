from django.db import models
from utilisateur.models import Utilisateur
# Create your models here.
class Notification(models.Model):

    id_notification=models.AutoField(primary_key=True)
    messsage=models.CharField(max_length=255)
    date=models.DateTimeField(auto_now_add=True)
    lu=models.BooleanField(default=False)
    utilisateur=models.ForeignKey(Utilisateur,on_delete=models.CASCADE,related_name='notifications')
    def envoyer_notification(self,utilisateur,message):
        notification=Notification(messsage=message)
        notification.save()
        # Logique pour envoyer la notification à l'utilisateur
    def marque_lue(self):
        self.lu=True
        self.save()    
    def __str__(self):
        return self.messsage

