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


User = get_user_model()


def note_liste(request):
    notes = Note.objects.all().order_by('-date_creation')
    return render(request, 'note/note_liste.html', {'notes': notes})

def recherche_notes(request):
    titre = request.GET.get('titre', '')
    categorie_id = request.GET.get('categorie', '')

    notes = Note.objects.all().order_by('-date_creation')
    categories = Categorie.objects.all()

    if titre:
        notes = notes.filter(titre__icontains=titre)

    if categorie_id:
        notes = notes.filter(categorie_id=categorie_id)

    return render(request, 'note/recherche_notes.html', {
        'notes': notes,
        'categories': categories,
        'titre': titre,
        'categorie_id': categorie_id,
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

        # couper les lignes longues
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

def note_detail(request, id):
    note = get_object_or_404(Note, id=id)
    medias = note.medias.all()
    partages = note.partages.all()
    versions = note.versions.all().order_by('-date_modification')

    return render(request, 'note/note_detail.html', {
        'note': note,
        'medias': medias,
        'partages': partages,
        'versions': versions,
    })


def note_ajouter(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)

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

            Version.objects.create(
                note=note,
                contenu=note.contenu
            )

            return redirect('note_liste')
    else:
        form = NoteForm()

    return render(request, 'note/note_form.html', {
        'form': form,
        'titre_page': 'Ajouter une note'
    })


def note_modifier(request, id):
    note = get_object_or_404(Note, id=id)

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

            return redirect('note_detail', id=note.id)
    else:
        form = NoteForm(instance=note)

    return render(request, 'note/note_form.html', {
        'form': form,
        'titre_page': 'Modifier une note'
    })


def note_supprimer(request, id):
    note = get_object_or_404(Note, id=id)

    if request.method == 'POST':
        note.delete()
        return redirect('note_liste')

    return render(request, 'note/note_supprimer.html', {'note': note})


def version(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    versions = Version.objects.filter(note=note).order_by('-date_modification')

    return render(request, 'note/versions.html', {
        'note': note,
        'versions': versions
    })
def media_liste(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    medias_internes = note.medias.filter(est_interne=True).order_by('-date_upload')
    medias_supplementaires = note.medias.filter(est_interne=False).order_by('-date_upload')

    contenu = note.contenu

    # Liens HTML : <a href="...">
    liens_html = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\']', contenu)

    # Liens écrits directement : https://...
    liens_textes = re.findall(r'https?://[^\s<>"\']+', contenu)

    # Fusionner sans doublons
    liens_internes = list(dict.fromkeys(liens_html + liens_textes))

    return render(request, 'note/media_liste.html', {
        'note': note,
        'medias_internes': medias_internes,
        'medias_supplementaires': medias_supplementaires,
        'liens_internes': liens_internes,
    })

def media_ajouter(request, note_id):
    note = get_object_or_404(Note, id=note_id)

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
def media_supprimer(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    note = media.note

    if request.method == 'POST':
        if media.image:
            media.image.delete(save=False)

        media.delete()
        return redirect('note_detail', id=note.id)

    return render(request, 'note/media_supprimer.html', {
        'media': media,
        'note': note
    })

def partage_ajouter(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == 'POST':
        form = PartageForm(request.POST)

        # Exclure l'utilisateur connecté de la liste des collaborateurs
        if request.user.is_authenticated:
            form.fields['collaborateur'].queryset = User.objects.exclude(id=request.user.id)
        else:
            form.fields['collaborateur'].queryset = User.objects.all()

        if form.is_valid():
            collaborateur = form.cleaned_data['collaborateur']

            # Vérifier si la note est déjà partagée avec ce collaborateur
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

                messages.success(request, "La note a été partagée avec succès.")
                return redirect('note_detail', id=note.id)

    else:
        form = PartageForm()

        # Exclure l'utilisateur connecté de la liste des collaborateurs
        if request.user.is_authenticated:
            form.fields['collaborateur'].queryset = User.objects.exclude(id=request.user.id)
        else:
            form.fields['collaborateur'].queryset = User.objects.all()

    return render(request, 'note/partage_form.html', {
        'form': form,
        'note': note
    })
def partage_modifier(request, partage_id):
    partage = get_object_or_404(Partage, id=partage_id)
    note = partage.note

    if request.method == 'POST':
        form = PartageForm(request.POST, instance=partage)

        if request.user.is_authenticated:
            form.fields['collaborateur'].queryset = User.objects.exclude(id=request.user.id)
        else:
            form.fields['collaborateur'].queryset = User.objects.all()

        if form.is_valid():
            form.save()
            messages.success(request, "La permission a été modifiée avec succès.")
            return redirect('note_detail', id=note.id)

    else:
        form = PartageForm(instance=partage)

        if request.user.is_authenticated:
            form.fields['collaborateur'].queryset = User.objects.exclude(id=request.user.id)
        else:
            form.fields['collaborateur'].queryset = User.objects.all()

    return render(request, 'note/partage_form.html', {
        'form': form,
        'note': note,
        'titre_page': 'Modifier la permission'
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