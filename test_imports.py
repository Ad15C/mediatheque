import os
import django

# Configurer Django avec les paramètres appropriés
os.environ['DJANGO_SETTINGS_MODULE'] = 'mediatheque_project.settings'
django.setup()

# Tester les imports après que Django soit configuré
try:
    from mediatheque_project.compte_emprunteur import views
    from mediatheque_project.gestion_mediatheque import urls

    print("Tous les imports fonctionnent correctement.")
except Exception as e:
    print(f"Erreur durant l'import : {e}")

