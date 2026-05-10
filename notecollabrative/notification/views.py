from django.shortcuts import render
from .models import Notification

def notifications(request):

    notifications = Notification.objects.all().order_by('-date')

    return render(
        request,
        'notification/notifications.html',
        {
            'notifications': notifications
        }
    )