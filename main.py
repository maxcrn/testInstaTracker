import os
from datetime import datetime, timedelta
from itertools import dropwhile, takewhile

import instaloader

# Credentials pour le login sur Google Vision
os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/maxcarin/Documents/Cours/M1 S2/Gestion de Projet/InstaTracker-d209c2a2aab7.json"

# Données en longitude et latitude de La Rochelle
lngLRMin = -1.234431
lngLRMax = -1.110850
latLRMin = 46.133955
latLRMax = 46.190103

L = instaloader.Instaloader()

# Login sur Instagram avec identifiant et mot de passe
L.login("instatrackeruppa", "instatracker")

## Pour télécharger un certain nombre de photos sur un hashtag ##
# L.download_hashtag('larochelletourisme', max_count=10)

#############################################################
## Pour télécharger des photos entre deux dates sur un hashtag ou un profil ##

# Spécification du hastag sur lequel télécharger les photos
#posts = L.get_hashtag_posts('larochelletourisme')
posts = L.get_hashtag_posts('larochelletourisme')

# Spécification du profil sur lequel télécharger les photos
# posts = instaloader.Profile.from_username(L.context, PROFILE).get_posts()

# Pour télécharger des photos entre deux dates sur un hashtag
# Corpus Francofolies
FIN = datetime(2019, 7, 13)
DEBUT = datetime(2019, 7, 10)

resInstaLoader = False
resGVision = False
i = 1

# Compteur de hotspots
compteurHSIL = {}
compteurHSGV = {}

# Booléen pour l'analyse de la trace
traceEnCours = False

for post in posts:
    # Condition sur la date du post
    if FIN >= post.date >= DEBUT:
        j = 1

        print("Photo " + str(i) + " ayant la date " + str(post.date))

        # Condition sur la localisation du post
        if post.location != None and lngLRMin < post.location.lng < lngLRMax and latLRMin < post.location.lat < latLRMax:
            print("Analyse InstaLoader : " + post.location.name)

            # Condition sur le nom de la localisation (si pas assez précis, envoi à Google Vision)
            if post.location.name == "La Rochelle, France":
                resGVision = detect_landmarks_uri(post.url)  # Analyse par Google Vision de la photo via son url
            else:
                resInstaLoader = True

        else:
            print("Pas de localisation InstaLoader")
            resGVision = detect_landmarks_uri(post.url)  # Analyse par Google Vision via son url

        # S'il y a une localisation précise sur la photo, on selectionne l'utilisateur et on analyse ses posts sur 2 jours
        if resGVision or resInstaLoader:
            # Compteur de hotspots
            if resInstaLoader:
                if (post.location.name in compteurHSIL):
                    compteurHSIL[post.location.name] += 1
                else:
                    compteurHSIL[post.location.name] = 1
            print(compteurHSGV)
            print(compteurHSIL)



# METTRE LES USERS DANS UN TABLEAU POUR NE PAS REFAIRE DEUX FOIS LE MEME


            print("")
            print("Analyse de la trace de l'utilisateur : " + post.owner_username)

            # Récupération du username et des posts correspondant
            utilActuel = post.owner_username
            postsUtilActuel = instaloader.Profile.from_username(L.context, utilActuel).get_posts()
            traceEnCours = True
            for postUtilActuel in postsUtilActuel:

                # Si la date d'un post est à J-2 ou J+2 de la date du post de base

                if post.date + timedelta(days=2) >= postUtilActuel.date >= post.date - timedelta(days=2):

                    print("Photo " + str(j) + " de l'analyse de la trace ayant la date " + str(postUtilActuel.date))

                    # Condition sur la localisation du post
                    if postUtilActuel.location != None \
                            and lngLRMin < postUtilActuel.location.lng < lngLRMax \
                            and latLRMin < postUtilActuel.location.lat < latLRMax:
                        print("Analyse InstaLoader : " + postUtilActuel.location.name)

                        # Condition sur le nom de la localisation (si pas assez précis, envoi à Google Vision)
                        if postUtilActuel.location.name == "La Rochelle, France":
                            # Analyse par Google Vision de la photo via son url
                            detect_landmarks_uri(postUtilActuel.url)


                    # S'il n'y avait pas de localisation de base, analyse par Google Vision
                    else:
                        print("Pas de localisation InstaLoader")
                        detect_landmarks_uri(postUtilActuel.url)

                    j = j + 1

            # On remet les varaibles de test à False
            resInstaLoader = False
            resGVision = False
            traceEnCours = False
            print("Fin de l'analyse de la trace utilisateur avec " + str(j) + " photos analysées")

        print("")
        i = i + 1


    # Fonction pour la detection des landmarks via Google Vision
    def detect_landmarks_uri(uri):
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = uri

        response = client.landmark_detection(image=image)
        landmarks = response.landmark_annotations
        if not (landmarks):
            print('Pas de landmark Google Vision')
        else:
            print("Landmark(s) Google Vision :")

        for landmark in landmarks:

            # Condition sur la longitude et latitude du landmark
            if lngLRMin < landmark.locations[0].lat_lng.longitude < lngLRMax \
                    and latLRMin < landmark.locations[0].lat_lng.latitude < latLRMax:
                print(landmark.description)  # Affichage du nom du hotspot
                print(landmark.locations[0].lat_lng.latitude)  # Affichage de la longitude du hotspot
                print(landmark.locations[0].lat_lng.longitude)  # Affichage de la latitude du hotspot
                print("Fin de l'analyse Google Vision")
                if not traceEnCours:
                    if(landmark.description in compteurHSGV):
                        compteurHSGV[landmark.description] += 1
                    else:
                        compteurHSGV[landmark.description] = 1
                return True
            else:
                print("Localisation hors La Rochelle")
                print("Fin de l'analyse Google Vision")
                return False


        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

