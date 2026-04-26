from django.shortcuts import render, get_object_or_404
from .models import Note, Version

def note_liste(request):
    notes = Note.objects.all()
    return render(request, 'note/note_liste.html', {'notes': notes})

def note_detail(request, id):
    note = get_object_or_404(Note, id=id)
    return render(request, 'note/note_detail.html', {'note': note})

def version(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    versions = Version.objects.filter(note=note).order_by('-date_modification')
    return render(request, 'note/versions.html', {
        'note': note,
        'versions': versions
    })