from django.db import models
from django.utils.timezone import now
from datetime import timedelta



# Classe représentant les médias (Livre, CD, DVD, Jeu de Plateau)
class Media(models.Model):
    TYPE_CHOICES = [
        ('Livre', 'Livre'),
        ('CD', 'CD'),
        ('DVD', 'DVD'),
        ('Jeu', 'Jeu de Plateau'),
    ]

    name = models.CharField(max_length=250)  # Nom du média
    type_media = models.CharField(max_length=10, choices=TYPE_CHOICES)  # Type du média
    date_emprunt = models.DateField(null=True, blank=True)  # Date de l'emprunt
    disponible = models.BooleanField(default=True)
    emprunteur = models.ForeignKey(
        'Emprunteur', null=True, blank=True, on_delete=models.SET_NULL
    )  # Lien vers l'emprunteur actuel (relation "un média <--> un emprunteur")

    # Champs supplémentaires pour décrire certains médias
    auteur = models.CharField(max_length=250, null=True, blank=True)
    artiste = models.CharField(max_length=250, null=True, blank=True)
    realisateur = models.CharField(max_length=250, null=True, blank=True)

    objects = models.Manager()
    pass

    def emprunter(self, emprunteur):
        if not self.disponible:
            raise ValueError("Ce média n'est pas disponible pour un emprunt.")
        if self.type_media == 'Jeu':
            raise ValueError("Les jeux de plateau ne peuvent pas être empruntés.")

        self.emprunteur = emprunteur
        self.date_emprunt = now().date()
        self.disponible = False
        self.save()


    def retourner(self):
        if self.emprunteur:
            self.emprunteur = None
            self.date_emprunt = None
            self.disponible = True
            self.save()


    def est_empruntable(self):
        if not self.disponible:
            return False, "Ce média est déjà emprunté."
        if self.type_media == 'Jeu':
            return False, "Les jeux de plateau ne peuvent pas être empruntés."
        return True, "Ce média est empruntable."

    def __str__(self):
        return f"{self.name} - {self.get_type_media_display()} ({'Disponible' if self.disponible else 'Emprunté'})"  # noqa: E1101


class Emprunteur(models.Model):
    STATUTS = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
    ]

    nom = models.CharField(max_length=250)
    prenom = models.CharField(max_length=250)
    date_naissance = models.DateField()
    adresse = models.TextField()
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    bloque = models.BooleanField(default=False)
    retard = models.BooleanField(default=False)
    statut = models.CharField(max_length=50, choices=STATUTS, default='actif')

    # Relation avec les médias empruntés
    emprunts = models.ManyToManyField(Media, related_name='emprunteurs', blank=True)
    objects = models.Manager()

    def statut_actuel(self):
        if self.bloque:
            return False, "Cet emprunteur est bloqué en raison d'emprunts dépassant le délai autorisé (7 jours)."
        if self.retard:
            return False, "Cet emprunteur est bloqué en raison d'emprunts retardés. Merci de retourner les médias empruntés pour débloquer l'accès."
        return "Actif"

    def verifier_statut(self):
        medias_en_retard = Media.objects.filter( # noqa: E1101
            emprunteur=self,
            disponible=False,
            date_emprunt__lt=now().date() - timedelta(days=7)
        )
        self.retard = medias_en_retard.exists()
        self.bloque = self.retard
        self.save()

    def peut_emprunter(self, media):
        self.verifier_statut()
        if self.bloque:
            return False, "L'emprunteur est bloqué."
        if self.retard:
            return False, "L'emprunteur a des emprunts en retard."
        if not media.disponible:
            return False, "Ce média n'est pas disponible."
        if media.type_media == 'Jeu':
            return False, "Les jeux de plateau ne peuvent pas être empruntés."
        limite_emprunts = 3
        emprunts_actifs = Media.objects.filter(emprunteur=self, disponible=False).count()
        if emprunts_actifs >= limite_emprunts:
            return False, f"La limite d'emprunts ({limite_emprunts}) a été atteinte."
        return True, "L'emprunteur peut emprunter ce média."

    def emprunter(self, media):
        peut_emprunter, message = self.peut_emprunter(media)
        if peut_emprunter:
            media.emprunter(self)
            self.save()
        else:
            raise ValueError(message)

    def retourner(self, media):
        if media.emprunteur != self:
            raise ValueError("Ce média n'a pas été emprunté par cet emprunteur.")
        media.retourner()
        self.save()

    def __str__(self):
        return f"{self.nom} {self.prenom} - {'Bloqué' if self.bloque else 'Autorisé'} - {'A du retard' if self.retard else 'À jour'}"
