from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from mediatheque_project.gestion_mediatheque.models import Media, Emprunteur
from mediatheque_project.gestion_mediatheque.forms import MediaForm



@login_required
def affichage_media(request):
    medias = Media.objects.all()
    return render(request, 'gestion_mediatheque/affichage_media.html', {'medias': medias})
pass


def ajouter_media(request):
    """Ajout d'un média """
    if request.method == "POST":
        # Crée une instance du formulaire avec les données soumises
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Média ajouté avec succès !")
            return redirect('affichage_media')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        # Formulaire vide lors d'une requête GET
        form = MediaForm()

    return render(request, 'gestion_mediatheque/ajouter_media.html', {'form': form})
pass


def emprunter_media(request, media_id, emprunteur_id):
    """Permet à un emprunteur d'emprunter un média disponible."""
    emprunteur = get_object_or_404(Emprunteur, pk=emprunteur_id)
    media = get_object_or_404(Media, pk=media_id)

    try:
        emprunteur.emprunter(media)  # Utilisation directe de la logique métier
        messages.success(request, f"{emprunteur.nom} a emprunté {media.name} avec succès.")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('affichage_media')
pass


def retourner_media(request, media_id):
    # Récupère le média ou renvoie une 404
    media = get_object_or_404(Media, id=media_id)
    try:
        if not media.disponible:
            # Vérifie que le média est emprunté
            media.retourner()
            # Appelle la méthode de retour sur le modèle
            messages.success(request, f"{media.name} a été retourné.")
        else:
            messages.error(request, "Ce média n'était pas emprunté.")
    except Exception as e:
        # Capture toute erreur imprévue
        messages.error(request, f"Une erreur est survenue : {str(e)}")
    # Redirige vers la page précédente ou unfallback

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
pass
