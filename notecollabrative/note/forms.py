from django import forms
from django.contrib.auth import get_user_model
from .models import Note, Categorie, Partage, Version, Media

User = get_user_model()


class NoteForm(forms.ModelForm):
    image_note = forms.ImageField(
        required=False,
        label="Image à insérer dans la note",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Note
        fields = ['titre', 'contenu', 'categorie']

        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de la note'
            }),
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'id': 'contenu-field',
                'placeholder': 'Écris ta note ici. Mets [IMAGE] à l’endroit où tu veux insérer l’image.'
            }),
            'categorie': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'description']

        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la catégorie'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description'
            }),
        }


class PartageForm(forms.ModelForm):
    collaborateur = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Collaborateur",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Partage
        fields = ['collaborateur', 'permission']

        widgets = {
            'permission': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['contenu']

        widgets = {
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Contenu de la version'
            }),
        }


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['type', 'url', 'image']

        widgets = {
            'type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ajouter un lien URL'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')
        image = cleaned_data.get('image')

        if not url and not image:
            raise forms.ValidationError("Veuillez ajouter soit un lien, soit une image.")

        return cleaned_data