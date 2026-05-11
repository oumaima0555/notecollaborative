from django.shortcuts import render, redirect, get_object_or_404
from .models import Commentaire
from .forms import CommentaireForm


# AJOUTER COMMENTAIRE
def ajouter_commentaire(request, note_id):

    form = CommentaireForm()

    if request.method == 'POST':

        form = CommentaireForm(request.POST)

        if form.is_valid():

            commentaire = form.save(commit=False)

            commentaire.utilisateur = request.user
            commentaire.note_id = note_id

            commentaire.save()

            return redirect('note_detail', note_id)

    return render(request, 'commentaire/commentaire_form.html', {
        'form': form
    })


# MODIFIER COMMENTAIRE
def modifier_commentaire(request, id):

    commentaire = get_object_or_404(Commentaire, pk=id)

    if request.method == 'POST':

        form = CommentaireForm(request.POST, instance=commentaire)

        if form.is_valid():

            form.save()

            return redirect('note_detail', commentaire.note.id)

    else:

        form = CommentaireForm(instance=commentaire)

    return render(request, 'commentaire/commentaire_form.html', {
        'form': form
    })


# SUPPRIMER COMMENTAIRE
def supprimer_commentaire(request, id):

    commentaire = get_object_or_404(Commentaire, pk=id)

    note_id = commentaire.note.id

    commentaire.delete()

    return redirect('note_detail', note_id)