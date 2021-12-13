from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.base import runTouchApp
from kivy.uix.spinner import Spinner

import sys
import random
import json

class Mastermind(App):
    """
    Classe principale du jeu.
    """
    def build(self):
        self.lines = []
        # Recherche et affichage du meilleur score.
        try:
            with open('data.json') as file:
                maxi = 0
                nommaxi = 0
                content = json.loads(file.read())
                for i in content.items():
                    if i[1]['Score'] > maxi:
                        maxi = i[1]['Score']
                        nommaxi = i[0]
        except FileNotFoundError:
            print('Le fichier est introuvable')
        except IOError:
            print("Erreur d'entrée/sortie")
        hasard()
        self.compteur = 0
        self.listereponse = []
        self.title = 'Mastermind'
        mainbox = BoxLayout(orientation= 'vertical')
        
        line1 = BoxLayout(orientation= 'horizontal')
        # Permet au joueur d'entrer son pseudo.
        self.pseudoinput = TextInput(hint_text= 'Pseudo', font_size='25', multiline= False, size_hint=(1,1), halign="center")
        self.record = Label(text= 'Record : ' + '{}/{}'.format(nommaxi, maxi))
        line1.add_widget(self.pseudoinput)
        line1.add_widget(self.record)

        line2 = BoxLayout(orientation= 'horizontal')
        propositionlabel = Label(text= 'Proposition', size_hint=(4, 1))
        oklabel = Label(text= 'OK')
        colorlabel = Label(text= 'Color')
        line2.add_widget(propositionlabel)
        line2.add_widget(oklabel)
        line2.add_widget(colorlabel)
        mainbox.add_widget(line1)
        mainbox.add_widget(line2)
        # Création de lignes dans une liste.
        for l in range(10):
            self.lines.append(BoxLayout(orientation= 'horizontal'))
            mainbox.add_widget(self.lines[l])

        line13 = BoxLayout(orientation= 'horizontal')
        # Création des spinners permettant au joueur de jouer des propositions de combinaisons.
        self.spinner0 = Spinner(text='', values=['Rouge', 'Jaune', 'Bleu', 'Orange', 'Rose', 'Vert'])
        self.spinner1 = Spinner(text='', values=['Rouge', 'Jaune', 'Bleu', 'Orange', 'Rose', 'Vert'])
        self.spinner2 = Spinner(text='', values=['Rouge', 'Jaune', 'Bleu', 'Orange', 'Rose', 'Vert'])
        self.spinner3 = Spinner(text='', values=['Rouge', 'Jaune', 'Bleu', 'Orange', 'Rose', 'Vert'])
        buttonspinner = Button(text='Valider', on_press= self.validation, size_hint=(2, 1))
        line13.add_widget(self.spinner0)
        line13.add_widget(self.spinner1)
        line13.add_widget(self.spinner2)
        line13.add_widget(self.spinner3)
        line13.add_widget(buttonspinner)

        mainbox.add_widget(line13)
        return mainbox

    def validation(self, source):
        # Gestion de l'erreur du spinner vide.
        if self.spinner0.text == '' or self.spinner1.text == '' or self.spinner2.text == '' or self.spinner3.text == '':
            pass
        # Ajout des couleurs dans chaque ligne en fonction du choix du joueur.
        else:
            #print(ordi)
            reponse = [self.spinner0.text, self.spinner1.text, self.spinner2.text, self.spinner3.text]
            #print(reponse)
            self.listereponse.append(reponse)
            for k in reponse:
                self.lines[self.compteur].add_widget(Image(source= "Couleurs/"+k+'.jpg'))
            self.lines[self.compteur].add_widget(Label(text= str(verif(ordi, reponse)[0])))
            self.lines[self.compteur].add_widget(Label(text= str(verif(ordi, reponse)[1])))
            # Quand le joueur gagne la partie.
            if verif(ordi, reponse)[0] == 4:
                # Extraction du fichier JSON déjà existant.
                try:
                    with open('data.json') as file:
                        self.dicodata = json.loads(file.read())
                except FileNotFoundError:
                    print('Le fichier est introuvable')
                except IOError:
                    print("Erreur d'entrée/sortie")
                # Modification du fichier JSON extrait précédemment en y ajoutant le nom, le score, la combinaison à trouver et les propositions du joueur.
                try:
                    with open('data.json', 'w') as file:
                        self.dicodata[self.pseudoinput.text] = {'Score': 10 - self.compteur, 'Combinaison': ordi, 'Propositions': self.listereponse}
                        file.write(json.dumps(self.dicodata, indent=4))
                except FileNotFoundError:
                    print('Le fichier est introuvable')
                except IOError:
                    print("Erreur d'entrée/sortie")

                App.get_running_app().stop()
                WinEnd().run()
                
            self.compteur += 1
        # Vérifie si le joueur a perdu.
        if self.compteur == 10:
            App.get_running_app().stop()
            LoseEnd().run()

class LoseEnd(App):
    """
    Classe de l'écran qui est affiché lorsque le joueur a perdu (fin de partie).
    """
    def build(self):
        box = BoxLayout(orientation= 'vertical')
        self.lose = Label(text= 'Game Over')
        line2 = BoxLayout(orientation= 'horizontal')
        self.boutonquit = Button(text= 'Quitter', on_press= self._quit)
        line2.add_widget(self.boutonquit)
        box.add_widget(self.lose)
        box.add_widget(line2)
        return box
        
    def _quit(self, source):
        sys.exit(0)
    
class WinEnd(App):
    """
    Classe de l'écran qui est affiché lorsque le joueur a gagné (fin de partie).
    """
    def build(self):
        box = BoxLayout(orientation= 'vertical')
        self.win = Label(text= 'Gagné !')
        line2 = BoxLayout(orientation= 'horizontal')
        self.boutonquit = Button(text= 'Quitter', on_press= self._quit)
        line2.add_widget(self.boutonquit)
        box.add_widget(self.win)
        box.add_widget(line2)
        return box
        
    def _quit(self, source):
        sys.exit(0)

def hasard():
    """
    Fonction qui utilise le module random pour selectionner une combinaison aléatoire en début de partie.
    """
    global ordi
    ordi = []
    i = 0
    while i < 4:
        ordi.append(random.choice(['Rouge', 'Bleu', 'Jaune', 'Vert','Rose', 'Orange']))
        i += 1
    return ordi

def verif(ordi, reponse):
    """
    Fonction qui vérifie le choix du joueur en fonction de la combinaison et qui retourne les indices.
    """
    mmc = 0
    mmp = 0
    ordicopie = ordi[:]
    for b in reponse:
        if b in ordicopie:
            mmc += 1
            ordicopie.remove(b)
    for c in range(4):
        if reponse[c] == ordi[c]:
            mmp += 1
    return [mmp, mmc - mmp]

Mastermind().run()