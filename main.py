# coding=utf-8
import json
import os
from datetime import datetime, timedelta
from tkinter import *
import tkinter.font as tkFont
from tkinter import filedialog
from instaloader import *
import os
import webbrowser
import folium

# Credentials pour le login sur Google Vision
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/maxcarin/Documents/Cours/M1 S2/Gestion de Projet/InstaTracker-d209c2a2aab7.json"

# Donnees en longitude et latitude de La Rochelle
lngLRMin = -1.234431
lngLRMax = -1.110850
latLRMin = 46.133955
latLRMax = 46.190103

global verifTermineBool

def openCollecte():

    collecteWindow = Toplevel()
    cadreCollecteHashtag = Frame(collecteWindow, width=500, height=500, borderwidth=1)
    cadreCollecteHashtag.pack(fill=BOTH)

    labelCollecte = Label(cadreCollecteHashtag, text="Collecte des données", font=titre1)
    labelCollecte.pack()

    choixHashtag = Label(cadreCollecteHashtag, text="Choix du hashtag : ")
    choixHashtag.pack(side="left")

    choixHashtagWrite = Entry(cadreCollecteHashtag, textvariable=hashtag, width=30)
    choixHashtagWrite.pack(side="right")

    hashtagAvantChamp = Label(cadreCollecteHashtag, text="#")
    hashtagAvantChamp.pack(side="right")

    cadreCollecteDates = Frame(collecteWindow, width=500, height=500, borderwidth=1)
    cadreCollecteDates.pack(fill=BOTH)

    datesCollecte = Label(cadreCollecteDates, text="Dates de la collecte", font=titre2)
    datesCollecte.pack(side="top")

    debut = Label(cadreCollecteDates, text="Début : ")
    debut.pack(side="left")


    dateDebutWrite = Entry(cadreCollecteDates, textvariable=dateDebut, width=30)
    dateDebutWrite.pack(side="left")

    dateFinWrite = Entry(cadreCollecteDates, textvariable=dateFin, width=30)
    dateFinWrite.pack(side="right")

    fin = Label(cadreCollecteDates, text="Fin : ")
    fin.pack(side="right")

    cadreCollecteValidation = Frame(collecteWindow, width=500, height=500, borderwidth=1)
    cadreCollecteValidation.pack(fill=BOTH)

    validation = Button(cadreCollecteValidation, text="Lancer la collecte", command=lambda : [collecte(), supprVerifText()])
    validation.pack(side="top")

    termineLabel = Label(cadreCollecteValidation, text="Collecte terminée")

    def verifTermine():
        print(verifTermineBool)
        if verifTermineBool:
            termineLabel.pack(side="right")
            verifTermineBouton.config(state="disabled")


    def supprVerifText():
        verifTermineBouton.config(state="normal")
        termineLabel.pack_forget()




    verifTermineBouton = Button(cadreCollecteValidation, text="Verifier si la collecte est terminée",
                                command=verifTermine, state = "disabled")
    verifTermineBouton.pack(side="left")




def openVisu():
    collecteWindow = Toplevel()

    cadreVisualisation = Frame(collecteWindow, width=500, height=500, borderwidth=1)
    cadreVisualisation.pack(fill=BOTH)

    labelVisu = Label(cadreVisualisation, text="Visualisation des données")
    labelVisu.pack()

    def openExplorateurCarte():
        filename = filedialog.askopenfilename(initialdir=(os.getcwd()+ "/Collectes"), title="Select file",
                                              filetypes=(("all files", ".html"), ("all files", ".*")))
        filenamePhoto = 'file:///' + filename
        webbrowser.open_new_tab(filenamePhoto)

    buttonVisuCarte = Button(cadreVisualisation, text="Selectionner une carte à afficher dans Traces", command=openExplorateurCarte)
    buttonVisuCarte.pack()

    global cadreJson
    cadreJson = Frame(collecteWindow, width=200, height=200, borderwidth=1)

    def openExplorateurJson():
        global cadreJson
        cadreJson.pack_forget()
        cadreJson = Frame(collecteWindow, width=200, height=200, borderwidth=1)
        cadreJson.pack(fill=BOTH)

        filename = filedialog.askopenfilename(initialdir=(os.getcwd()+ "/Collectes"), title="Select file",
                                              filetypes=(("all files", ".json"), ("all files", ".*")))

        Label(cadreJson, text="Hotspots").grid(column=1, row=1)
        Label(cadreJson, text="Nombre d'apparitions").grid(column=2, row=1)

        with open(filename) as json_file:
            data = json.load(json_file)
        print(data)

        k = 2

        for i in data:
            Label(cadreJson, text=i).grid(column=1, row=k)
            Label(cadreJson, text=data[i]).grid(column=2, row=k)
            k = k + 1

    buttonVisuJson = Button(cadreVisualisation, text="Selectionner un fichier de hostpots à afficher", command=openExplorateurJson)
    buttonVisuJson.pack()


def openAccueil():
    cadre = Frame(app, width=500, height=500, borderwidth=1)
    cadre.pack(fill=BOTH)

    label = Label(cadre, text="InstaTracker", font=titre1)
    label.pack(side="top")

    collecteBouton = Button(cadre, text="Collecte des données", command=openCollecte)
    collecteBouton.pack(side="left")

    visuBouton = Button(cadre, text="Visualisation des données", command=openVisu)
    visuBouton.pack(side="right")


def collecte():


    global verifTermineBool # Utilisation de la variable globale trace

    # Tableau de couleurs pour le tracé de la carte
    color = ['black', 'red', 'blue', 'green', 'gold', 'darkorchild', 'deepskyblue',
             'sandybrown', 'olivedrab', 'palevioletred', 'seagreen', 'sienna', 'cyan',
             'indigo', 'magenta', 'orange', 'indianred', 'lightstillblue', 'thistle', 'yellow']



    verifTermineBool = False
    hashtagCollecte = hashtag.get()

    L = instaloader.Instaloader()

    # Login sur Instagram avec identifiant et mot de passe
    L.login("instatrackeruppa", "instatracker")

    ## Pour télécharger un certain nombre de photos sur un hashtag ##
    # L.download_hashtag('larochelletourisme', max_count=10)

    #############################################################
    ## Pour télécharger des photos entre deux dates sur un hashtag ou un profil ##

    # Spécification du hastag sur lequel télécharger les photos
    #posts = L.get_hashtag_posts('toursaintnicolas')
    #posts = L.get_hashtag_posts('larochelletourisme')
    posts = L.get_hashtag_posts(hashtagCollecte)

    # Spécification du profil sur lequel télécharger les photos
    # posts = instaloader.Profile.from_username(L.context, PROFILE).get_posts()

    # Pour télécharger des photos entre deux dates sur un hashtag
    # Corpus Francofolies
    dateDebutString = dateDebut.get()
    dateFinString = dateFin.get()

    debutJour = int(dateDebutString[:2])
    debutMois = int(dateDebutString[3:5])
    debutAnnee = int(dateDebutString[6:10])

    finJour = int(dateFinString[:2])
    finMois = int(dateFinString[3:5])
    finAnnee = int(dateFinString[6:10])

    FIN = datetime(finAnnee, finMois, finJour)
    DEBUT = datetime(debutAnnee, debutMois, debutJour)

    debutFormat = DEBUT.strftime("%d-%m-%Y")
    finFormat = FIN.strftime("%d-%m-%Y")


    resInstaLoader = False
    resGVision = False
    i = 1


    # Compteur de hotspots
    compteurHSIL = {}
    compteurHSGV = {}
    hotspots = {}

    # Suivi de trace
    traces = {}

    # Booléen pour l'analyse de la trace
    traceEnCours = False

    def correctionTrace(traceTableau):
        tableauCorrige = []
        for i in (traceTableau):
            if "Lanterne" in i[0] or "lanterne" in i[0]:
                tableauCorrige.append(["Tour de la Lanterne", 46.1557861, -1.1570111])

            elif "Horloge" in i[0] or "horloge" in i[0]:
                tableauCorrige.append(["La Grosse Horloge", 46.1583799, -1.1560111])

            elif "Nicolas" in i[0] or "nicolas" in i[0]:
                tableauCorrige.append(["Tour St-Nicolas", 46.1557685, -1.1555935])

            elif "Port" in i[0] or "port" in i[0] or "Tour" in i[0] or "tour" in i[0] or "Harbour" in i[
                0] or "harbour" in i[0] \
                    or "Towers" in i[0] or "towers" in i[0]:
                tableauCorrige.append(["Port de La Rochelle", 46.1582234, -1.1548676])

            elif "Aquarium" in i[0] or "aquarium" in i[0]:
                tableauCorrige.append(["Aquarium de La Rochelle", 46.1532698, -1.1527392])

            elif "Gabut" in i[0] or "gabut" in i[0]:
                tableauCorrige.append(["Le Gabut", 46.1523002, -1.1555237])

            elif "Minimes" in i[0] or "minimes" in i[0]:
                tableauCorrige.append(["Les Minimes", 46.1430282, -1.1732062])

            else:
                tableauCorrige.append(i)

        return tableauCorrige

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
                traceTemp = []
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
                            else:
                                traceTemp.append([postUtilActuel.location.name, postUtilActuel.location.lat,
                                                  postUtilActuel.location.lng])

                        # S'il n'y avait pas de localisation de base, analyse par Google Vision
                        else:
                            print("Pas de localisation InstaLoader")
                            detect_landmarks_uri(postUtilActuel.url)

                        j = j + 1

                if len(traceTemp) > 3:
                    traceTempClean = correctionTrace(traceTemp)
                    traces[post.owner_username] = traceTempClean

                # On remet les varaibles de test à False
                resInstaLoader = False
                resGVision = False
                traceEnCours = False
                print("Fin de l'analyse de la trace utilisateur avec " + str(j-1) + " photos analysées")

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
                        if (landmark.description in compteurHSGV):
                            compteurHSGV[landmark.description] += 1
                        else:
                            compteurHSGV[landmark.description] = 1
                    else:
                        traceTemp.append([landmark.description, landmark.locations[0].lat_lng.latitude,
                                          landmark.locations[0].lat_lng.longitude])
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

    def creationCompteur(compteur):
        # key : values
        for i in (compteur):
            if "Lanterne" in i or "lanterne" in i:
                if "Tour de la Lanterne" in hotspots:
                    hotspots["Tour de la Lanterne"] += compteur[i]
                else:
                    hotspots["Tour de la Lanterne"] = compteur[i]
            elif "Horloge" in i or "horloge" in i:
                if "La Grosse Horloge" in hotspots:
                    hotspots["La Grosse Horloge"] += compteur[i]
                else:
                    hotspots["La Grosse Horloge"] = compteur[i]

            elif "Nicolas" in i or "nicolas" in i:
                if "Tour St-Nicolas" in hotspots:
                    hotspots["Tour St-Nicolas"] += compteur[i]
                else:
                    hotspots["Tour St-Nicolas"] = compteur[i]

            elif "Port" in i or "port" in i or "Tour" in i or "tour" in i or "Harbour" in i or "harbour" in i \
                    or "Towers" in i or "towers" in i:
                if "Port de La Rochelle" in hotspots:
                    hotspots["Port de La Rochelle"] += compteur[i]
                else:
                    hotspots["Port de La Rochelle"] = compteur[i]

            elif "Aquarium" in i or "aquarium" in i:
                if "Aquarium de La Rochelle" in hotspots:
                    hotspots["Aquarium de La Rochelle"] += compteur[i]
                else:
                    hotspots["Aquarium de La Rochelle"] = compteur[i]

            elif "Gabut" in i or "gabut" in i:
                if "Le Gabut" in hotspots:
                    hotspots["Le Gabut"] += compteur[i]
                else:
                    hotspots["Le Gabut"] = compteur[i]

            elif "Minimes" in i or "minimes" in i:
                if "Les Minimes" in hotspots:
                    hotspots["Les Minimes"] += compteur[i]
                else:
                    hotspots["Les Minimes"] = compteur[i]

            else:
                if i in hotspots:
                    hotspots[i] += compteur[i]
                else:
                    hotspots[i] = compteur[i]

    creationCompteur(compteurHSIL)
    creationCompteur(compteurHSGV)
    print(hotspots)
    print(traces)

    cheminDossier = "Collectes/#" + hashtagCollecte + str(debutFormat) + "_" + str(finFormat) + "/"

    if not os.path.exists(cheminDossier):
        os.makedirs(cheminDossier, 0o777)

    if not os.path.exists(cheminDossier + "Hotspots/"):
        os.makedirs(cheminDossier + "Hotspots/", 0o777)

    if not os.path.exists(cheminDossier + "Traces/"):
        os.makedirs(cheminDossier + "Traces/", 0o777)

    with open(cheminDossier + "Traces/" + "#" + hashtagCollecte + "_" + "traces_" + str(debutFormat) + "_" + str(finFormat) + ".json", "w") as write_file:
        json.dump(traces, write_file)

    with open(cheminDossier + "Hotspots/" + "#" + hashtagCollecte + "_" + "hotspots_" + str(debutFormat) + "_" + str(finFormat) + ".json", "w") as write_file:
        json.dump(hotspots, write_file)

    with open(cheminDossier + "Hotspots/" + "#" + hashtagCollecte + "_" + "nombrePhotosHotspots" + str(debutFormat) + "_" + str(finFormat) + ".json", "w") as write_file:
        json.dump(i-1, write_file)

    c = folium.Map(location=[46.158152, -1.151455], zoom_start=14) # Création de la carte

    colorNb = 0 # Compteur de couleurs à 0

    # Création des traces sur la carte
    for i in traces:
        # On remet la 1ere couleur s'il y a eu plus de 20 traces
        if colorNb > 19 :
            colorNb = 0

        intermediaire = []
        k = 0

        # Création des points
        for j in traces[i]:
            intermediaire.append([j[1], j[2]])
            print(intermediaire)
            folium.Circle(radius=10, location=intermediaire[k], color="red", popup=j[0]).add_to(c)
            k = k + 1

        # Création des lignes
        folium.PolyLine(intermediaire, popup=i, color=color[colorNb]).add_to(c)
        colorNb = colorNb + 1

    # Sauvegarde de la carte
    c.save(cheminDossier + "Traces/" + "#" + hashtagCollecte + "_" + "hotspots_" + str(debutFormat) + "_" + str(finFormat) + '.html')


    verifTermineBool = True
    print(verifTermineBool)


app = Tk()
hashtag = StringVar()
dateDebut = StringVar()
dateFin = StringVar()
verifTermineBool = None
titre1 = tkFont.Font(family='Helvetica', size=48, weight='bold')
titre2 = tkFont.Font(family='Helvetica', size=36, weight='bold')


openAccueil()

app.mainloop()
