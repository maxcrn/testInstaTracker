import os
from datetime import datetime
from itertools import dropwhile, takewhile

import instaloader

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/maxcarin/Documents/Cours/M1 S2/Gestion de Projet/InstaTracker-d209c2a2aab7.json"

# Données en longitude et latitude de La Rochelle
lngLRMin = -1.234431
lngLRMax = -1.110850
latLRMin = 46.133955
latLRMax = 46.190103

# Pour que le json soit bien formaté et non compressé
L = instaloader.Instaloader(compress_json=False)

# Login sur Instagram avec identifiant et mot de passe
L.login("instatrackeruppa", "instatracker")
## Pour télécharger un certain nombre de photos sur un hashtag ##
# L.download_hashtag('larochelletourisme', max_count=10)

#############################################################
## Pour télécharger des photos entre deux dates sur un hashtag ou un profil ##

# Spécification du hastag sur lequel télécharger les photos
posts = L.get_hashtag_posts('larochelletourisme')

# Spécification du profil sur lequel télécharger les photos
# posts = instaloader.Profile.from_username(L.context, PROFILE).get_posts()

# Pour télécharger des photos entre deux dates sur un hashtag
FIN = datetime(2020, 2, 25)
DEBUT = datetime(2020, 2, 21)

for post in posts:
    if FIN >= post.date >= DEBUT:  # Condition sur la date du post
        print(post.date)
        # Condition sur la localisation du post
        if post.location != None and lngLRMin < post.location.lng < lngLRMax and latLRMin < post.location.lat < latLRMax:
            print(post.location)
            #L.download_post(post, '#larochelletourisme')
            # Condition sur le nom de la localisation (si pas assez précis, envoi à Google Vision)
            if post.location.name == "La Rochelle, France":
                detect_landmarks_uri(post.url)  # Analyse par Google Vision de la photo via son url
        else:
            detect_landmarks_uri(post.url)  # Analyse par Google Vision via son url


    # Fonction pour la detection des landmarks via Google Vision
    def detect_landmarks_uri(uri):
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = uri

        response = client.landmark_detection(image=image)
        landmarks = response.landmark_annotations
        print('Landmarks:')

        for landmark in landmarks:
            print(landmark.description) # Affichage du nom du hotspot
            print(landmark.locations[0].lat_lng.latitude) # Affichage de la longitude du hotspot
            print(landmark.locations[0].lat_lng.longitude) # Affichage de la latitude du hotspot

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
