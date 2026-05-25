"""
URL configuration for notecollabrative project.
"""

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('utilisateur.urls')),
    path('admin/', admin.site.urls),
    path('note_liste/', include('note.urls')),
    path('tags/', include('tag.urls')),
    path('commentaires/', include('commentaire.urls')),
    path('notifications/', include('notification.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)