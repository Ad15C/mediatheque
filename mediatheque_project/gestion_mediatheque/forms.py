from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Media, Emprunteur


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        # Inclure tous les champs du modèle Media
        fields = '__all__'

    def clean_name(self):
        """Validation pour empêcher les noms de médias d'être vides ou constitués uniquement d'espaces."""
        name = self.cleaned_data.get('name', '')
        if not name.strip():
            raise ValidationError("Le nom du média ne peut pas être vide.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        type_media = cleaned_data.get('type_media')

        if type_media == 'Jeu':
            raise ValidationError("Les jeux de plateau ne peuvent pas être empruntés.")
        return cleaned_data


class EmprunteurForm(forms.ModelForm):
    class Meta:
        model = Emprunteur
        # Champs affichés dans le formulaire
        fields = ['nom', 'prenom', 'date_naissance', 'adresse', 'phone', 'email', 'statut']
        # Libellés personnalisés pour améliorer l'affichage
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'date_naissance': 'Date de Naissance',
            'adresse': 'Adresse',
            'phone': 'Téléphone',
            'email': 'Courriel',
            'statut': 'Statut',
        }

    def clean_date_naissance(self):
        """Vérifie que la date de naissance n'est pas dans le futur."""
        date_naissance = self.cleaned_data['date_naissance']
        if date_naissance and date_naissance > date.today():
            raise ValidationError("La date de naissance ne peut pas être dans le futur.")
        return date_naissance

    def clean(self):
        """Validation globale : vérifie qu'au moins un contact est fourni (email ou téléphone)."""
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        email = cleaned_data.get("email")

        if not phone and not email:
            raise ValidationError("Vous devez fournir au moins un numéro de téléphone ou un email.")
        return cleaned_data
