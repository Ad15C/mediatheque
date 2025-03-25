from django.urls import path
from mediatheque_project.gestion_mediatheque import (
    liste_emprunteurs,
    ajouter_emprunteur,
    modifier_emprunteur
)

from mediatheque_project.gestion_mediatheque import (
    affichage_media,
    ajouter_media,
    emprunter_media,
    retourner_media,
)

from mediatheque_project.gestion_mediatheque import tableau_de_bord_personnel

urlpatterns = [
    # URLs pour les emprunteurs
    path('emprunteurs/', liste_emprunteurs, name='liste_emprunteurs'),
    path('emprunteurs/ajouter/', ajouter_emprunteur, name='ajouter_emprunteur'),
    path('emprunteurs/modifier/<int:emprunteur_id>/', modifier_emprunteur, name='modifier_emprunteur'),

    # URLs pour les médias
    path('medias/', affichage_media, name='affichage_media'),
    path('medias/ajouter/', ajouter_media, name='ajouter_media'),
    path('medias/emprunter/<int:media_id>/<int:emprunteur_id>/', emprunter_media, name='emprunter_media'),
    path('medias/retourner/<int:media_id>/', retourner_media, name='retourner_media'),

    # URL pour le personnel
    path('personnel/dashboard/', tableau_de_bord_personnel, name='tableau_de_bord_personnel'),
]

