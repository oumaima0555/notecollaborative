from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Commentaire
from .forms import CommentaireForm

from note.models import Note, Partage


def peut_gerer_commentaire(user, note):
    """
    Autoriser l'ajout, la modification et la suppression d'un commentaire
    seulement si l'utilisateur a la permission commentaire ou edition.
    """

    # Si l'utilisateur est le propriétaire de la note
    if note.utilisateur == user:
        return True

    # Vérifier le partage avec le collaborateur
    partage = Partage.objects.filter(
        note=note,
        collaborateur=user
    ).first()

    if partage and partage.permission in ['commentaire', 'edition', 'édition']:
        return True

    return False


# AJOUTER COMMENTAIRE
@login_required
def ajouter_commentaire(request, note_id):

    note = get_object_or_404(Note, pk=note_id)

    if not peut_gerer_commentaire(request.user, note):
        messages.error(request, "Vous n'avez pas la permission d'ajouter un commentaire.")
        return redirect('note_detail', note_id)

    if request.method == 'POST':

        form = CommentaireForm(request.POST)

        if form.is_valid():

            commentaire = form.save(commit=False)
            commentaire.utilisateur = request.user
            commentaire.note = note
            commentaire.save()

            return redirect('note_detail', note_id)

    else:
        form = CommentaireForm()

    return render(request, 'commentaire/commentaire_form.html', {
        'form': form,
        'note': note
    })


# MODIFIER COMMENTAIRE
@login_required
def modifier_commentaire(request, id):

    commentaire = get_object_or_404(Commentaire, pk=id)
    note = commentaire.note

    if not peut_gerer_commentaire(request.user, note):
        messages.error(request, "Vous n'avez pas la permission de modifier ce commentaire.")
        return redirect('note_detail', note.id)

    if request.method == 'POST':

        form = CommentaireForm(request.POST, instance=commentaire)

        if form.is_valid():

            form.save()

            return redirect('note_detail', note.id)

    else:

        form = CommentaireForm(instance=commentaire)

    return render(request, 'commentaire/commentaire_modifier.html', {
        'form': form,
        'commentaire': commentaire,
        'note': note
    })


# SUPPRIMER COMMENTAIRE
@login_required
def supprimer_commentaire(request, id):

    commentaire = get_object_or_404(Commentaire, pk=id)
    note = commentaire.note

    if not peut_gerer_commentaire(request.user, note):
        messages.error(request, "Vous n'avez pas la permission de supprimer ce commentaire.")
        return redirect('note_detail', note.id)

    if request.method == 'POST':
        commentaire.delete()
        messages.success(request, "Le commentaire a été supprimé avec succès.")
        return redirect('note_detail', note.id)

    return render(request, 'commentaire/commentaire_confirm_delete.html', {
        'commentaire': commentaire,
        'note': note
    })