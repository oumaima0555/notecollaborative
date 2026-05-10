from django.shortcuts import render, redirect, get_object_or_404
#ajouetr par salma pour verifier les permissions du utilisateur avant de lui permettre d'ajouter un commentaire
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#la fin de l'ajout de salma
from note.models import Note, Partage
from .models import Commentaire
from .forms import CommentaireForm


@login_required
def ajouter_commentaire(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    # Vérifier les permissions de l'utilisateur pour commenter la note ajouter par salma/ila bghiti tzidi modifier commentaire awla suuprimer commentaire khas verification de permission dial utilisateur
    est_proprietaire = note.utilisateur == request.user

    peut_commenter = Partage.objects.filter(
        note=note,
        collaborateur=request.user,
        permission__in=['commentaire', 'edition']
    ).exists()

    if not est_proprietaire and not peut_commenter:
        messages.error(request, "Vous n'avez pas la permission de commenter cette note.")
        return redirect('note_detail', id=note.id)
#la fin
    if request.method == 'POST':
        form = CommentaireForm(request.POST)

        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.note = note
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