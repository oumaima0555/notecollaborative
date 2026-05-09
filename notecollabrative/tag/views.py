from django.shortcuts import render, redirect, get_object_or_404
from .models import Tag
from .forms import TagForm

# Liste des tags
def liste_tags(request):
    tags = Tag.objects.all()
    return render(request, 'tag/liste_tags.html', {'tags': tags})

# Ajouter tag
def ajouter_tag(request):

    if request.method == 'POST':
        form = TagForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('tags:liste_tags')

    else:
        form = TagForm()

    return render(request, 'tags/tag_form.html', {'form': form})

# Modifier
def modifier_tag(request, id):

    tag = get_object_or_404(Tag, id=id)

    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)

        if form.is_valid():
            form.save()
            return redirect('tags:liste_tags')

    else:
        form = TagForm(instance=tag)

    return render(request, 'tags/tag_form.html', {'form': form})

# Supprimer
def supprimer_tag(request, id):

    tag = get_object_or_404(Tag, id=id)

    if request.method == 'POST':
        tag.delete()
        return redirect('tags:liste_tags')

    return render(request, 'tags/tag_delete.html', {'tag': tag})