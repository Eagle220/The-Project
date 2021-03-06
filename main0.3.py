# codind:utf8

"""

- transformer
- rajouter équivalence soif --> boisson, alim --> faim
- voir pour remplacer le scan par mesure de distances-
- ameliorer choix ressource

- rajouter gestion bords carte
- rajouter gestin vitesse
"""

from math import sqrt
from random import randint
import os
from time import clock

class Ressources(object):

    """Objet ressource"""

    def __init__(self, nom, type_source, position, quantite, vitesse_regen):

        self.nom = nom
        self.type = type_source
        self.posx = position[0]
        self.posy = position[1]
        self.quantite = quantite
        self.vitesse_regen = vitesse_regen

    def __repr__(self):

        return "Source de %s, situee a (%s,%s), avec %s de %s" % (
            self.type, self.posx, self.posy, self.quantite, self.nom)

    def utilisation_source(self, pion):

        if self.quantite > 0:
            self.maxi = pion.besoins[self.type][1]
            self.courant = pion.besoins[self.type][0]
            self.a_remplir = self.maxi - self.courant

            if self.quantite < self.a_remplir:
                self.quantite_livree = self.quantite

            elif self.quantite >= self.a_remplir:
                self.quantite_livree = self.a_remplir

            pion.besoins[self.type][0] += self.quantite_livree
            self.quantite -= self.quantite_livree
            print("La source de regenere de  %s %s" %
                  (self.quantite_livree, self.type))
            print("Etat apres source : ", pion.besoins)
        else:
            print("Source vide")

    def regeneration(self):
        self.quantite += self.vitesse_regen


class Pion(object):

    """ objet pion"""

    def __init__(self, nom, pos_init=[0, 0], vision=2, besoins={}):
        self.nom = nom
        self.posx = pos_init[0]
        self.posy = pos_init[1]
        self.vitesse = 1
        self.age = 0
        self.etat = True

        self.vision = vision
        self.besoins = besoins
        self.besoin_a_combler = min(self.besoins)

    def __repr__(self):
        return "%s, situe en (%s,%s) avec %s" % (self.nom, self.posx, self.posy, self.besoins)

    def deter_etat(self):
        for elem in self.besoins:
            if self.besoins[elem][0] <= 0:

                self.etat = False

        return self.etat

    def update_pion(self):


        """fnct qui update la pos du pion a chaque tour"""
        print("         %s\n" % (self.nom))
        print("Position debut : %s, %s " % (self.posx, self.posy))
        print("Etat debut : ", self.besoins, "\n")

        self.besoin_a_combler = min(self.besoins)
        self.analyse_chp_visions(ressources_carte)

        if self.ressource_chp_vision != []:
            print("Sources a portee : ", self.ressource_chp_vision)
            self.choix_source(self.ressource_chp_vision)
            print("Source choisie : ", self.source_choisie)

            self.deplace_elem(self.source_choisie)
            print("Position finale : %s, %s " % (self.posx, self.posy))
            self.usure()

            if (self.posx, self.posy) == (self.source_choisie.posx, self.source_choisie.posy):
                """ on est sur une source non vide, on l'utilise"""
                self.source_choisie.utilisation_source(pion1)

        else:
            print("Pas de source trouvee a proximite.")
            self.deplace_aleat()
            print("Position finale : %s, %s " % (self.posx, self.posy))
            self.usure()


    def analyse_chp_visions(self, ressources):

        self.limite_inf_x = int(self.posx - self.vision)
        self.limite_sup_x = int(self.posx + self.vision)

        self.limite_sup_y = int(self.posy + self.vision)
        self.limite_inf_y = int(self.posy - self.vision)

        self.ressource_chp_vision = []

        self.distances = []
        self.type_sources = []

        for k in range(self.limite_inf_x, self.limite_sup_x):
            for j in range(self.limite_inf_y, self.limite_sup_y):
                for elem in ressources:

                    pos = (elem.posx, elem.posy)
                    if pos == (k, j) and pos != (self.posx, self.posy):
                        distance = sqrt((elem.posx - self.posx)**2 +
                                        (elem.posy - self.posy)**2)

                        self.ressource_chp_vision.append(elem)
                        self.distances.append(int(distance))

                        self.type_sources.append(elem.type)
        # print(distance)

    def choix_source(self, sources):

        self.plus_proche = self.distances.index(min(self.distances))
        
        self.besoin_urgent = min(besoins.items(), key=lambda x: x[1][0]) 


        self.source_choisie = self.ressource_chp_vision[self.plus_proche]

    def _get_pos_dest_relat(self, source):

        self.depl_x = source.posx - self.posx
        self.depl_y = source.posy - self.posy
        print("deplacement necessaire: ", self.depl_x, self.depl_y)

    def deplace_elem(self, source):
        self._get_pos_dest_relat(source)

        if self.depl_x == self.depl_y:

            self.posx += int(self.depl_x / abs(self.depl_x))
            self.posy += int(self.depl_y / abs(self.depl_y))

        elif self.depl_x > self.depl_y:
            self.posx += int(self.depl_x / abs(self.depl_x))

        else:
            self.posy += int(self.depl_y / abs(self.depl_y))

    def deplace_aleat(self, *args):

        if len(args) > 0:
            direction = args[0]
        else:
            direction = randint(0, 5)

        if direction == 0:
            self.posx += 1
            self.posy += 0

        elif direction == 1:
            self.posx += 0
            self.posy += 1

        elif direction == 2:
            self.posx += -1
            self.posy += 0

        elif direction == 3:
            self.posx += 0
            self.posy += -1

        elif direction == 4:
            self.posx += -1
            self.posy += -1
        elif direction == 5:
            self.posx += 1
            self.posy += 1

    def usure(self, intensite=1):

        self.besoins["faim"][0] -= 10 * intensite
        self.besoins["soif"][0] -= 10 * intensite
        print("Le deplacement coute %s de besoins" % (10 * intensite))
        print("Etat apres deplacement : ", self.besoins, "\n")


def update_source():
    for elem in ressources_carte:
        elem.regeneration()


def update_pions(liste, tour):
    ranj = range(len(liste_pions))

    for j in reversed(ranj):
        
        liste_pions[j].deter_etat()
        if liste_pions[j].etat:
            liste_pions[j].update_pion()
        else:
            print(liste_pions[j].nom, "est mort")
            liste.append([liste_pions[j].nom, tour])
            liste_pions.remove(liste_pions[j])


viande1 = Ressources("viande1", "faim", (0, 0), 10, 5)
eau1 = Ressources("eau1", "soif", (2, 2), 1000, 10)
ressources_carte = [viande1, eau1]

besoins = {"faim": [100, 100], "soif": [100, 100]}

pion1 = Pion("Captain America", [100, 100], 5, {"faim": [100, 100], "soif": [100, 100]})
pion2 = Pion("Iron Man", [90, 90], 5, {"faim": [100, 100], "soif": [100, 100]})

liste_pions = [pion1, pion2]
liste_tour_mort = []

tour = 0
t0 = clock()


while len(liste_pions) > 0:
    print("------------------------- Tour n %s ------------------------- " % (tour))
    update_pions(liste_tour_mort, tour)
    update_source()
    tour += 1
    print("\n")
t1 = clock()

print (t1-t0)