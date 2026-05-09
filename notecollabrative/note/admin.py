from django.contrib import admin
from .models import Note, Categorie, Partage, Version, Media

admin.site.register(Note)
admin.site.register(Categorie)
admin.site.register(Partage)
admin.site.register(Version)
admin.site.register(Media)