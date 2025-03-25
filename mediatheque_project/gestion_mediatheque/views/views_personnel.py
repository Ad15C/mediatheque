from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


# Fonction pour vérifier si l'utilisateur fait partie du groupe "Personnel"
def est_bibliothecaire(user):
    return user.is_authenticated and user.groups.filter(name="Personnel").exists()


@login_required
@user_passes_test(est_bibliothecaire)
def tableau_de_bord_personnel(request):
    """ Affiche le tableau de bord pour les membres du personnel."""
    return render(request, 'personnel/tableau_de_bord.html')
