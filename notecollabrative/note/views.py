from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Note, Version, Media, Partage, Categorie
from .forms import NoteForm, VersionForm, MediaForm, PartageForm, CategorieForm
from django.db.models import Q
from django.http import HttpResponse
from django.utils.html import strip_tags
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import re
from tag.models import Tag
from django.contrib.auth.decorators import login_required
from notification.models import Notification


User = get_user_model()


def nom_utilisateur(user):
    if user.get_full_name():
        return user.get_full_name()
    return user.username


@login_required
def note_liste(request):
    if request.user.is_superuser:
        notes = Note.objects.all().order_by('-date_creation')
    else:
        notes = Note.objects.filter(
            utilisateur=request.user,
            partages__isnull=True
        ).distinct().order_by('-date_creation')

    return render(request, 'note/note_liste.html', {
        'notes': notes
    })


def recherche_notes(request):
    titre = request.GET.get('titre', '')
    categorie_id = request.GET.get('categorie', '')
    tag_id = request.GET.get('tag', '')

    notes = Note.objects.all().order_by('-date_creation')
    categories = Categorie.objects.all()
    tags = Tag.objects.all()

    if titre:
        notes = notes.filter(titre__icontains=titre)

    if categorie_id:
        notes = notes.filter(categorie_id=categorie_id)

    if tag_id:
        notes = notes.filter(tags__id_tag=tag_id)

    return render(request, 'note/recherche_notes.html', {
        'notes': notes,
        'categories': categories,
        'tags': tags,
        'titre': titre,
        'categorie_id': categorie_id,
        'tag_id': tag_id,
    })


def exporter_markdown(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    contenu_sans_html = strip_tags(note.contenu)

    markdown_content = f"""# {note.titre}

**Catégorie :** {note.categorie.nom if note.categorie else 'Aucune'}

**Date création :** {note.date_creation.strftime('%d/%m/%Y %H:%M')}

**Date modification :** {note.date_modification.strftime('%d/%m/%Y %H:%M')}

---

{contenu_sans_html}
"""

    response = HttpResponse(markdown_content, content_type='text/markdown; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{note.titre}.md"'
    return response


def exporter_pdf(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{note.titre}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    largeur, hauteur = A4

    y = hauteur - 50

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, note.titre)
    y -= 30

    p.setFont("Helvetica", 10)

    categorie = note.categorie.nom if note.categorie else "Aucune"
    p.drawString(50, y, f"Catégorie : {categorie}")
    y -= 20

    p.drawString(50, y, f"Date création : {note.date_creation.strftime('%d/%m/%Y %H:%M')}")
    y -= 20

    p.drawString(50, y, f"Date modification : {note.date_modification.strftime('%d/%m/%Y %H:%M')}")
    y -= 30

    contenu = strip_tags(note.contenu)

    p.setFont("Helvetica", 11)

    lignes = contenu.splitlines()

    for ligne in lignes:
        if y < 50:
            p.showPage()
            y = hauteur - 50
            p.setFont("Helvetica", 11)

        while len(ligne) > 90:
            p.drawString(50, y, ligne[:90])
            ligne = ligne[90:]
            y -= 15

            if y < 50:
                p.showPage()
                y = hauteur - 50
                p.setFont("Helvetica", 11)

        p.drawString(50, y, ligne)
        y -= 15

    p.showPage()
    p.save()
    return response


@login_required
def note_detail(request, id):
    if request.user.is_superuser:
        note = get_object_or_404(Note, id=id)
    else:
        note = get_object_or_404(
            Note.objects.filter(
                Q(utilisateur=request.user) | Q(partages__collaborateur=request.user)
            ).distinct(),
            id=id
        )

    # Médias internes seulement pour le détail
    medias = note.medias.filter(est_interne=True)

    partages = note.partages.all()
    versions = note.versions.all().order_by('-date_modification')

    est_proprietaire = note.utilisateur == request.user or request.user.is_superuser

    partage_user = Partage.objects.filter(
        note=note,
        collaborateur=request.user
    ).first()

    permission_user = partage_user.permission if partage_user else None

    # Contenu affiché dans la page détail
    contenu_note_detail = note.contenu

    # Supprimer du contenu les médias externes ajoutés depuis "Ajouter média"
    medias_externes = note.medias.filter(est_interne=False)

    for media in medias_externes:

        # Si le média externe est une image
        if media.image:
            image_url = media.image.url

            contenu_note_detail = re.sub(
                r'<img[^>]*src=["\']' + re.escape(image_url) + r'["\'][^>]*>',
                '',
                contenu_note_detail
            )

        # Si le média externe est un lien
        if media.url:
            url = media.url

            contenu_note_detail = re.sub(
                r'<a[^>]*href=["\']' + re.escape(url) + r'["\'][^>]*>.*?</a>',
                '',
                contenu_note_detail
            )

            contenu_note_detail = contenu_note_detail.replace(url, '')

    return render(request, 'note/note_detail.html', {
        'note': note,
        'contenu_note_detail': contenu_note_detail,
        'medias': medias,
        'partages': partages,
        'versions': versions,
        'est_proprietaire': est_proprietaire,
        'permission_user': permission_user,
    })


@login_required
def note_ajouter(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)

        if form.is_valid():
            note = form.save(commit=False)
            note.utilisateur = request.user
            note.save()

            form.save_m2m()

            image_note = form.cleaned_data.get('image_note')

            if image_note:
                media = Media.objects.create(
                    note=note,
                    type='image',
                    image=image_note,
                    est_interne=True
                )

                image_html = f'<img src="{media.image.url}" style="max-width:300px; border-radius:10px;">'

                if '[IMAGE]' in note.contenu:
                    note.contenu = note.contenu.replace('[IMAGE]', image_html, 1)
                else:
                    note.contenu += '<br><br>' + image_html

                note.save()

            Version.objects.create(
                note=note,
                contenu=note.contenu
            )

            Notification.objects.create(
                utilisateur=request.user,
                messsage=f"{nom_utilisateur(request.user)} a ajouté une nouvelle note"
            )

            return redirect('note_liste')

    else:
        form = NoteForm()

    return render(request, 'note/note_form.html', {
        'form': form,
        'titre_page': 'Ajouter une note'
    })


@login_required
def note_modifier(request, id):
    note = get_object_or_404(Note, id=id)

    est_proprietaire = note.utilisateur == request.user

    a_permission_edition = Partage.objects.filter(
        note=note,
        collaborateur=request.user,
        permission='edition'
    ).exists()

    if not est_proprietaire and not a_permission_edition:
        messages.error(request, "Vous n'avez pas la permission de modifier cette note.")
        return redirect('note_detail', id=note.id)

    if request.method == 'POST':
        ancien_contenu = note.contenu

        form = NoteForm(request.POST, request.FILES, instance=note)

        if form.is_valid():
            note = form.save()

            image_note = form.cleaned_data.get('image_note')

            if image_note:
                media = Media.objects.create(
                    note=note,
                    type='image',
                    image=image_note,
                    est_interne=True
                )

                image_html = f'<img src="{media.image.url}" style="max-width:300px; border-radius:10px;">'

                if '[IMAGE]' in note.contenu:
                    note.contenu = note.contenu.replace('[IMAGE]', image_html, 1)
                else:
                    note.contenu += '<br><br>' + image_html

                note.save()

            if ancien_contenu != note.contenu:
                Version.objects.create(
                    note=note,
                    contenu=note.contenu
                )

                Notification.objects.create(
                    utilisateur=request.user,
                    messsage=f"{nom_utilisateur(request.user)} a modifié une note"
                )

            return redirect('note_detail', id=note.id)

    else:
        form = NoteForm(instance=note)

    return render(request, 'note/note_form.html', {
        'form': form,
        'titre_page': 'Modifier une note'
    })


@login_required
def note_supprimer(request, id):
    note = get_object_or_404(Note, id=id)

    if note.utilisateur != request.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer cette note.")
        return redirect('note_detail', id=note.id)

    if request.method == 'POST':
        Notification.objects.create(
            utilisateur=request.user,
            messsage=f"{nom_utilisateur(request.user)} a supprimé une note"
        )

        note.delete()

        return redirect('note_liste')

    return render(request, 'note/note_supprimer.html', {
        'note': note
    })


def version(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    versions = Version.objects.filter(note=note).order_by('-date_modification')

    return render(request, 'note/versions.html', {
        'note': note,
        'versions': versions
    })


@login_required
def media_liste(request, note_id):
    if request.user.is_superuser:
        note = get_object_or_404(Note, id=note_id)
    else:
        note = get_object_or_404(
            Note.objects.filter(
                Q(utilisateur=request.user) | Q(partages__collaborateur=request.user)
            ).distinct(),
            id=note_id
        )

    medias_internes = note.medias.filter(est_interne=True).order_by('-date_upload')
    medias_supplementaires = note.medias.filter(est_interne=False).order_by('-date_upload')

    contenu = note.contenu

    liens_html = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\']', contenu)
    liens_textes = re.findall(r'https?://[^\s<>"\']+', contenu)
    liens_internes = list(dict.fromkeys(liens_html + liens_textes))

    est_proprietaire = note.utilisateur == request.user or request.user.is_superuser

    partage_user = Partage.objects.filter(
        note=note,
        collaborateur=request.user
    ).first()

    permission_user = partage_user.permission if partage_user else None

    return render(request, 'note/media_liste.html', {
        'note': note,
        'medias_internes': medias_internes,
        'medias_supplementaires': medias_supplementaires,
        'liens_internes': liens_internes,
        'est_proprietaire': est_proprietaire,
        'permission_user': permission_user,
    })


@login_required
def media_ajouter(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    est_proprietaire = note.utilisateur == request.user

    a_permission_edition = Partage.objects.filter(
        note=note,
        collaborateur=request.user,
        permission='edition'
    ).exists()

    if not est_proprietaire and not a_permission_edition:
        messages.error(request, "Vous n'avez pas la permission d'ajouter un média.")
        return redirect('note_detail', id=note.id)

    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)

        if form.is_valid():
            media = form.save(commit=False)
            media.note = note
            media.est_interne = False
            media.save()
            return redirect('note_detail', id=note.id)

    else:
        form = MediaForm()

    return render(request, 'note/media_form.html', {
        'form': form,
        'note': note
    })


@login_required
def media_supprimer(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    note = media.note

    est_proprietaire = note.utilisateur == request.user

    a_permission_edition = Partage.objects.filter(
        note=note,
        collaborateur=request.user,
        permission='edition'
    ).exists()

    if not est_proprietaire and not a_permission_edition:
        messages.error(request, "Vous n'avez pas la permission de supprimer ce média.")
        return redirect('note_detail', id=note.id)

    if request.method == 'POST':
        if media.image:
            media.image.delete(save=False)

        media.delete()
        return redirect('note_detail', id=note.id)

    return render(request, 'note/media_supprimer.html', {
        'media': media,
        'note': note
    })


@login_required
def partage_ajouter(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if note.utilisateur != request.user:
        messages.error(request, "Seul le propriétaire peut partager cette note.")
        return redirect('note_detail', id=note.id)

    if request.method == 'POST':
        form = PartageForm(request.POST)
        form.fields['collaborateur'].queryset = User.objects.exclude(id=request.user.id)

        if form.is_valid():
            collaborateur = form.cleaned_data['collaborateur']

            partage_existe = Partage.objects.filter(
                note=note,
                collaborateur=collaborateur
            ).exists()

            if partage_existe:
                messages.error(request, "Cette note est déjà partagée avec ce collaborateur.")
            else:
                partage = form.save(commit=False)
                partage.note = note
                partage.save()

                Notification.objects.create(
                    utilisateur=collaborateur,
                    messsage=f"{nom_utilisateur(request.user)} a partagé une note avec vous : {note.titre}"
                )

                messages.success(request, "La note a été partagée avec succès.")
                return redirect('note_detail', id=note.id)

    else:
        form = PartageForm()
        form.fields['collaborateur'].queryset = User.objects.exclude(id=request.user.id)

    return render(request, 'note/partage_form.html', {
        'form': form,
        'note': note
    })


@login_required
def partage_modifier(request, partage_id):
    partage = get_object_or_404(Partage, id=partage_id)
    note = partage.note

    if note.utilisateur != request.user:
        messages.error(request, "Seul le propriétaire peut modifier les permissions.")
        return redirect('note_detail', id=note.id)

    if request.method == 'POST':
        form = PartageForm(request.POST, instance=partage)
        form.fields['collaborateur'].queryset = User.objects.exclude(id=request.user.id)

        if form.is_valid():
            form.save()
            messages.success(request, "La permission a été modifiée avec succès.")
            return redirect('note_detail', id=note.id)

    else:
        form = PartageForm(instance=partage)
        form.fields['collaborateur'].queryset = User.objects.exclude(id=request.user.id)

    return render(request, 'note/partage_form.html', {
        'form': form,
        'note': note,
        'titre_page': 'Modifier la permission'
    })


@login_required
def partage_supprimer(request, partage_id):
    partage = get_object_or_404(Partage, id=partage_id)
    note = partage.note

    if note.utilisateur != request.user:
        messages.error(request, "Seul le propriétaire peut supprimer ce partage.")
        return redirect('note_detail', id=note.id)

    if request.method == 'POST':
        collaborateur = partage.collaborateur
        partage.delete()

        Notification.objects.create(
            utilisateur=collaborateur,
            messsage=f"Le partage de la note '{note.titre}' a été supprimé."
        )

        messages.success(request, "Le partage a été supprimé avec succès.")
        return redirect('note_detail', id=note.id)

    return render(request, 'note/partage_supprimer.html', {
        'partage': partage,
        'note': note
    })


def categorie_liste(request):
    categories = Categorie.objects.all()

    return render(request, 'note/categorie_liste.html', {
        'categories': categories
    })


def categorie_ajouter(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('categorie_liste')

    else:
        form = CategorieForm()

    return render(request, 'note/categorie_form.html', {
        'form': form
    })


def categorie_modifier(request, id):
    categorie = get_object_or_404(Categorie, id=id)

    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)

        if form.is_valid():
            form.save()
            return redirect('categorie_liste')

    else:
        form = CategorieForm(instance=categorie)

    return render(request, 'note/categorie_form.html', {
        'form': form,
        'titre_page': 'Modifier une catégorie'
    })


def categorie_supprimer(request, id):
    categorie = get_object_or_404(Categorie, id=id)

    if request.method == 'POST':
        categorie.delete()
        return redirect('categorie_liste')

    return render(request, 'note/categorie_supprimer.html', {
        'categorie': categorie
    })


@login_required
def collaborations_avec_moi(request):
    if request.user.is_superuser:
        collaborations = Partage.objects.all().select_related(
            'note',
            'collaborateur'
        ).order_by('-date_partage')
    else:
        collaborations = Partage.objects.filter(
            Q(collaborateur=request.user) | Q(note__utilisateur=request.user)
        ).select_related(
            'note',
            'collaborateur'
        ).order_by('-date_partage')

    return render(request, 'note/collaborations_avec_moi.html', {
        'collaborations': collaborations
    })