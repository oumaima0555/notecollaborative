from django.shortcuts import render, redirect, get_object_or_404
from .models import Commentaire
from .forms import CommentaireForm
from note.models import Note

from django.shortcuts import render, redirect, get_object_or_404
from note.models import Note
from .models import Commentaire
from .forms import CommentaireForm


def ajouter_commentaire(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == 'POST':
        form = CommentaireForm(request.POST)

        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.note = note

            if request.user.is_authenticated:
                commentaire.utilisateur = request.user

            commentaire.save()
#hna modifit ghir smia dial page hit smitha note_detail 
            return redirect('note_detail', id=note.id)

    else:
        form = CommentaireForm()

    return render(request, 'commentaire/commentaire_form.html', {
        'form': form,
        #whna zadt note bach tla3 lia f note
        'note': note
    })