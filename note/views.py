from django.shortcuts import render, get_object_or_404, redirect
from .models import Note


def note_list(request):
    notes = Note.objects.all().order_by('-date_creation')
    return render(request, 'note/note_list.html', {'notes': notes})


def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'note/note_detail.html', {'note': note})


def note_create(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenu = request.POST.get('contenu')

        if titre and contenu:
            Note.objects.create(titre=titre, contenu=contenu)
            return redirect('note_list')

    return render(request, 'note/note_create.html')

# Create your views here.
