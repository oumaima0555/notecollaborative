from django.shortcuts import render, redirect, get_object_or_404
from .models import Commentaire
from .forms import CommentaireForm
from note.models import Note

def ajouter_commentaire(request, note_id):

    note = get_object_or_404(Note, id=note_id)

    if request.method == 'POST':

        form = CommentaireForm(request.POST)

        if form.is_valid():

            commentaire = form.save(commit=False)

            commentaire.note = note

            commentaire.utilisateur = request.user

            commentaire.save()

            return redirect('note:detail_note', id=note.id)

    else:
        form = CommentaireForm()

    return render(request,
                  'commentaire/commentaire_form.html',
                  {'form': form})