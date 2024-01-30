from Constants import *
from Player import *

class WayOut:

    def __init__(self, maze, player):
        
        self.grille = maze.maze
        self.player = player
        
        self.largeur_grille = len(self.grille[1])
        self.hauteur_grille = len(self.grille)
        print("Largeur:", self.largeur_grille)
        print("Hauteur:", self.hauteur_grille)
        for i in range(len(self.grille)):
            print(self.grille[i])
        # Position de départ du joueur, lors de l'ouverture du jeu
        self.position_depart = self.position('S')
        # Position de fin dans la grille, lors de l'ouverture du jeu
        self.position_sortie = self.position('E')

        self.start = [
            (self.position_depart[1] + 0.2) * (WIDTH / self.largeur_grille),
            (self.position_depart[0] + 0.2) * (HEIGHT / self.hauteur_grille)
        ]

        self.taille_joueur_x = int(PLAYER_SIZE * (WIDTH / self.largeur_grille))
        self.taille_joueur_y = int(PLAYER_SIZE * (HEIGHT / self.hauteur_grille))

        #print("Largeur: ", self.largeur_grille)
        #print("Hauteur: ", self.hauteur_grille)

        chemin_solution = self.profondeur_abord(self.position_depart, [])
        self.distance_max = 3

        print("Chemin:", chemin_solution)

        # Convertir les positions du chemin vers les indications de déplacement avec ajustement pour la taille du joueur et la vitesse
        self.indications_deplacement = []

        for i in range(1, len(chemin_solution)):
            directions = self.convertir_direction(
                chemin_solution[i - 1], chemin_solution[i], self.distance_max
            )
            self.indications_deplacement.extend(directions)
            #self.indications_deplacement.extend(self.centre(chemin_solution[i]))

        # print("Chemin vers la sortie:", chemin_solution)
        #print("Indications de déplacement (avec ajustement pour la taille du joueur):", self.indications_deplacement)
        # print("Position initiale du joueur dans la tuile 'S':", self.start)

    def return_way(self):
        return self.indications_deplacement

    def nombre_element(self):
        return len(self.indications_deplacement)

    def position(self, element):
        for i, ligne in enumerate(self.grille):
            for j, case in enumerate(ligne):
                if case == element:
                    return (i, j)
                
    def centre(self, position_chemin):
        x, y = self.player.get_position()
        position_centrer_y = position_chemin[0]*(HEIGHT / self.hauteur_grille)
        position_centrer_x = position_chemin[1]*(WIDTH / self.largeur_grille)

        directions = []
        deplacement = 0

        if x - position_centrer_x > 0:
            deplacement = (x - position_centrer_x) / self.distance_max
            directions.extend(['LEFT'] * 2)
        if x - position_centrer_x < 0:
            deplacement = (position_centrer_x - x) / self.distance_max
            print("Deplacement:", deplacement)
            directions.extend(['RIGHT'] * 2)
        if y - position_centrer_y > 0:
            deplacement = (y - position_centrer_y) / self.distance_max
            directions.extend(['UP'] * 2)
        if y - position_centrer_y < 0:
            deplacement = (position_centrer_y - y) / self.distance_max
            directions.extend(['DOWN'] * 2)

        return directions

    def sortie(self, position):
        return position == self.position_sortie

    def valide(self, position):
        i, j = position
        return (
                0 <= i < len(self.grille) and
                0 <= j < len(self.grille[0]) and
                (self.grille[i][j] != '1')
        # Ajout de la condition pour les artefacts, tresors
        )

    def deplacements_possibles(self, position):
        i, j = position
        deplacements = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        return [p for p in deplacements if self.valide(p)]

    def profondeur_abord(self, position_actuelle, chemin):
        if self.sortie(position_actuelle):
            return chemin + [position_actuelle]

        for prochaine_position in self.deplacements_possibles(position_actuelle):
            if prochaine_position not in chemin:
                nouveau_chemin = self.profondeur_abord(prochaine_position, chemin + [position_actuelle])
                if nouveau_chemin:
                    return nouveau_chemin

        return None

    def convertir_direction(self, ancienne_position, nouvelle_position, distance_max):
        i_old, j_old = ancienne_position
        i_new, j_new = nouvelle_position

        directions = []
        ajout = 0

        # Calcul de la distance en pixels entre les tuiles en fonction de la taille du joueur

        #Si on descend
        if j_old == j_new and i_old + 1 == i_new:
            nb_deplacement = ((i_new * (HEIGHT / self.hauteur_grille))) - ((i_old * (HEIGHT / self.hauteur_grille)))
            
            nb = (nb_deplacement / distance_max)

            if (nb - int(nb)) > 0.5 and ajout == 0:
                nb = nb + 1
                ajout = ajout + 1

            directions.extend(['DOWN'] * int(nb))
            #directions.extend(['DOWN'] * 5)
            nb_deplacement = 0
            nb = 0

        #Si on tourne droite
        if j_old + 1 == j_new and i_old == i_new:
            nb_deplacement = ((j_new * (WIDTH / self.largeur_grille))) - ((j_old * (WIDTH / self.largeur_grille)))
            nb = (nb_deplacement / distance_max)

            #if (nb - int(nb)) > 0:
            #    nb = nb + 1

            directions.extend(['RIGHT'] * int(nb))
            nb_deplacement = 0
            nb = 0

        #Si on monte
        if j_old == j_new and i_old - 1 == i_new:
            nb_deplacement = ((i_old * (HEIGHT / self.hauteur_grille))) - ((i_new * (HEIGHT / self.hauteur_grille)))
            nb = (nb_deplacement / distance_max)

            if (nb - int(nb)) > 0.5:
                nb = nb + 1

            directions.extend(['UP'] * int(nb))
            nb_deplacement = 0
            nb = 0

        #Si on tourne gauche
        if j_old - 1 == j_new and i_old == i_new:
            nb_deplacement = ((j_old * (WIDTH / self.largeur_grille))) - ((j_new * (WIDTH / self.largeur_grille)))
            nb = (nb_deplacement / distance_max)

            #if (nb - int(nb)) > 0:
            #    nb = nb + 1

            directions.extend(['LEFT'] * int(nb))
            nb_deplacement = 0
            nb = 0

        print(directions)

        print("Change mouvement")
        return directions
    
    def reenitialisation(self, joueur, map, item, nbr):


        #Deplacement de recuperation
        j_x, j_y = joueur.get_position()
        i_x = item[0][0]
        i_y = item[0][1]

        if ((i_x - j_x) > (self.taille_joueur_x - 2) and self.indications_deplacement[nbr] != 'RIGHT') or ((i_x - j_x) < (-self.taille_joueur_x + 2) and self.indications_deplacement[nbr] != 'LEFT') or ((i_y - j_y) > (self.taille_joueur_y - 2) and self.indications_deplacement[nbr] != 'DOWN') or ((i_y - j_y) < (-self.taille_joueur_y+2) and self.indications_deplacement[nbr] != 'UP'):
            print("rentre")
            self.indications_deplacement.clear()

            directions = []
            directionB = []

            # Si on doit descendre
            if i_y > j_y:
                nb_deplacement = (i_y - j_y)
                nb = (nb_deplacement / self.distance_max)

                #if (nb - int(nb)) > 0:
                #    nb = nb + 1

                directions.extend(['DOWN'] * int(nb))
                #directionB.extend(['UP'] * int(nb))
                nb_deplacement = 0
                nb = 0
        
            # Si on doit tourner droite
            if i_x > j_x:
                nb_deplacement = (i_x - j_x)
                nb = (nb_deplacement / self.distance_max)

                #if (nb - int(nb)) > 0:
                #    nb = nb + 1

                directions.extend(['RIGHT'] * int(nb))
                #directionB.extend(['LEFT'] * int(nb))
                nb_deplacement = 0
                nb = 0
            
            # Si on doit tourner gauche
            if i_x < j_x:
                nb_deplacement = (j_x - i_x) 
                nb = (nb_deplacement / self.distance_max)
                directions.extend(['LEFT'] * int(nb))
                #directionB.extend(['RIGHT'] * int(nb))
                nb_deplacement = 0
                nb = 0
            
            # Si on doit monter
            if i_y < j_y:
                nb_deplacement = (j_y - i_y)
                nb = (nb_deplacement / self.distance_max)

                #if (nb - int(nb)) > 0:
                #    nb = nb + 1

                directions.extend(['UP'] * int(nb))
                #directionB.extend(['DOWN'] * int(nb))
                nb_deplacement = 0
                nb = 0
        
            self.indications_deplacement.extend(directions)
            print("Direction:", directions)
            directions.clear()
            #self.indications_deplacement.extend(directionB)
            return 0
        return nbr
    
    def restart(self, player):
        x, y = player.get_position()
        
        self.position_depart = (int(y/(HEIGHT / self.hauteur_grille)),int(x/(WIDTH / self.largeur_grille)))
        print("Nouvelle position:",self.position_depart)

        self.indications_deplacement.clear()

        chemin_solution = self.profondeur_abord(self.position_depart, [])

        for i in range(1, len(chemin_solution)):
            directions = self.convertir_direction(
                chemin_solution[i - 1], chemin_solution[i], self.distance_max
            )
            self.indications_deplacement.extend(directions)
        print("Nouvelle grille:", self.indications_deplacement)
        return 0
    
    def effacement(self):
        print("effacement")
        self.indications_deplacement.clear()

    def ajoutParcours(self, value, player, nb):
        self.indications_deplacement.clear()
        x, y = player.get_position()
        print("Nouvelle valeur:", value)
        directions = []
        directions.extend([value] * nb)
        print(directions)
        self.indications_deplacement.extend(directions)

        self.position_depart = (int(y/(HEIGHT / self.hauteur_grille)),int(x/(WIDTH / self.largeur_grille)))

        print("Position de départ:", self.position_depart)

        chemin_solution = self.profondeur_abord(self.position_depart, [])

        for i in range(1, len(chemin_solution)):
            directions = self.convertir_direction(
                chemin_solution[i - 1], chemin_solution[i], self.distance_max
            )
            self.indications_deplacement.extend(directions)
        print("Nouvelle grille:", self.indications_deplacement)
        return 0