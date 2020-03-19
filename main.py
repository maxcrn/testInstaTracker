from datetime import datetime
from itertools import dropwhile, takewhile

import instaloader

# Login sur Instagram avec identifiant et mot de passe
L.login("instatrackeruppa", "instatracker")

# Pour que le json soit bien formaté et non compressé
L = instaloader.Instaloader(compress_json=False)

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
    if FIN >= post.date >= DEBUT:
        print(post.date)
        L.download_post(post, '#larochelletourisme')
