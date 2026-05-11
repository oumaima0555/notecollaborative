from django.shortcuts import render, redirect, get_object_or_404
#ajouetr par salma pour verifier les permissions du utilisateur avant de lui permettre d'ajouter un commentaire
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#la fin de l'ajout de salma
from note.models import Note, Partage
from .models import Commentaire
from .forms import CommentaireForm

from django.shortcuts import render, redirect, get_object_or_404

# Décorateur pour obliger l'utilisateur à être connecté
from django.contrib.auth.decorators import login_required

# Messages d'erreur ou de succès
from django.contrib import messages

# Importer Note et Partage pour vérifier les permissions
from note.models import Note, Partage

from .models import Commentaire
from .forms import CommentaireForm

#ouma hna dart des modifs 3la 9bal les permissions
@login_required
def ajouter_commentaire(request, note_id):
    # Récupérer la note concernée par le commentaire
    note = get_object_or_404(Note, id=note_id)

    # Vérifier si l'utilisateur connecté est un administrateur
    est_admin = request.user.is_superuser

    # Vérifier si l'utilisateur connecté est le propriétaire de la note
    est_proprietaire = note.utilisateur == request.user

    # Vérifier si l'utilisateur connecté est collaborateur
    # avec une permission qui lui permet de commenter
    peut_commenter = Partage.objects.filter(
        note=note,
        collaborateur=request.user,
        permission__in=['commentaire', 'edition']
    ).exists()

    # Si l'utilisateur n'est ni admin, ni propriétaire,
    # ni collaborateur autorisé, on bloque l'accès
    if not est_admin and not est_proprietaire and not peut_commenter:
        messages.error(request, "Vous n'avez pas la permission de commenter cette note.")
        return redirect('note_detail', id=note.id)

    # Si le formulaire est envoyé
    if request.method == 'POST':
        form = CommentaireForm(request.POST)

        # Vérifier si les données du formulaire sont valides
        if form.is_valid():
            commentaire = form.save(commit=False)

            # Lier le commentaire à la note actuelle
            commentaire.note = note

            # Lier le commentaire à l'utilisateur connecté
            commentaire.utilisateur = request.user

            # Enregistrer le commentaire dans la base de données
            commentaire.save()

            # Retourner vers la page détail de la note
            return redirect('note_detail', id=note.id)

    else:
        # Si la page est ouverte avec GET, afficher un formulaire vide
        form = CommentaireForm()

    # Afficher la page du formulaire de commentaire
    return render(request, 'commentaire/commentaire_form.html', {
        'form': form,
        'note': note
    })