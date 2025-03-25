from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q  # Pour gérer la recherche
from django.contrib.auth.decorators import login_required

# Imports depuis notre application
from mediatheque_project.gestion_mediatheque.models import Emprunteur, Media
from mediatheque_project.gestion_mediatheque.forms import EmprunteurForm



@login_required
def liste_medias(request):
    medias = Media.objects.all()
    return render(request, 'gestion_mediatheque/affichage_medias.html', {'medias': medias})




#Vues des emprunteurs
"""Ajouter emprunteur"""
def ajouter_emprunteur(request):
    if request.method == "POST":
        form = EmprunteurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Emprunteur ajouté avec succès !")
            return redirect('liste_emprunteurs')
        else:
            messages.error(request, "Des erreurs ont été détectées. Veuillez corriger.")
    else:
        form = EmprunteurForm()
    return render(request, 'gestion_mediatheque/ajouter_emprunteur.html', {'form': form})
pass



"""Affichage de la liste des emprunteurs"""
def liste_emprunteurs(request):
    query = request.GET.get('q', '')  # Récupération de la recherche
    emprunteurs_query = Emprunteur.objects.prefetch_related('emprunts')

    # Si une recherche est effectuée
    if query:
        emprunteurs_query = emprunteurs_query.filter(
            Q(nom__icontains=query) | Q(prenom__icontains=query)
        )

    # Pagination : 10 emprunteurs par page
    paginator = Paginator(emprunteurs_query, 10)
    page_number = request.GET.get('page')  # Numéro de la page actuelle
    emprunteurs = paginator.get_page(page_number)  # Récupération des emprunteurs pour cette page

    # Passer la liste paginée et la recherche au template
    return render(request, 'gestion_mediatheque/liste_emprunteur.html', {'emprunteurs': emprunteurs, 'query': query})
pass


"""Mise à jour d'un profile emprunteur'"""
def modifier_emprunteur(request, emprunteur_id):
    emprunteur = get_object_or_404(Emprunteur, id=emprunteur_id)
    if request.method == 'POST':  # Si le formulaire a été soumis (méthode POST)
        form = EmprunteurForm(request.POST, instance=emprunteur)
        if form.is_valid():  # Validation du formulaire
            form.save()  # Sauvegarde des changements de l'emprunteur
            messages.success(request, "Emprunteur modifié avec succès.")
            return redirect('liste_emprunteurs')  # Retourne vers la liste des emprunteurs
        else:
            messages.error(request, "Des erreurs ont été détectées. Veuillez corriger.")
    else:  # Affichage initial avec les données existantes de l'emprunteur
        form = EmprunteurForm(instance=emprunteur)

    return render(request, 'gestion_mediatheque/modifier_emprunteur.html', {'form': form})
pass

