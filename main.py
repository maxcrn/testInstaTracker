from datetime import datetime
from itertools import dropwhile, takewhile

import instaloader

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
    if FIN >= post.date >= DEBUT: # Condition sur la date du post
        print(post.date)
        # Condition sur la localisation du post
        if post.location != None and lngLRMin < post.location.lng < lngLRMax and latLRMin < post.location.lat < latLRMax:
            print(post.location)
            L.download_post(post, '#larochelletourisme')
            # Condition sur le nom de la localisation (si pas assez précis, envoi à Google Vision)
            if post.location.name == "La Rochelle, France":
                print("Passage dans Google Vision")
        else:
            print("Passage dans Google Vision")


