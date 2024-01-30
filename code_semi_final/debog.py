from Maze import *
from Player import *
from IA import *
from WayOut import *

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class Debog:
    def __init__(self):
        self.position_joueur_x = 0
        self.position_joueur_y = 0
        self.wall_colision = []
        self.position_wall_col_x = 0 # wall position in x for collision
        self.position_wall_col_y = 0 # wall position in y for collision
        self.pos_wall_player_x = 0
        self.pos_wall_player_y = 0
        self.wall_list_x = []
        self.wall_list_y = []
        self.old_way = ''
        self.compteur = 0
    
    # Cette fonction est appeler afin de permettre au joueur de sortie d une impace
    def escape_wall(self, player, maze, wall_list, ia):
        print("Collision Detected!")

        ia.effacement()

        col_point = player.get_rect().collideobjects(maze.wallList)
        self.position_joueur_x, self.position_joueur_y = player.get_position()
        
        self.position_joueur_grille = (int(self.position_joueur_y/(maze.tile_size_y)),int(self.position_joueur_x/(maze.tile_size_x)))
        print("Nouvelle position:",self.position_joueur_grille)

        print("Position joueur:", player.get_position())
       
        print("Position wall:", wall_list)
        elements_uniques = []
        for rect in wall_list:
            if rect not in elements_uniques:
                elements_uniques.append(rect)
        nb = len(elements_uniques)
        for i in range(nb):
            vrx = int(wall_list[i][0]/(maze.tile_size_x))
            vry = int(wall_list[i][1]/(maze.tile_size_y))
            vrx1 = wall_list[i][0]
            vry1 = wall_list[i][1]
            if ((wall_list[i][0]/(maze.tile_size_x)) - int(wall_list[i][0]/(maze.tile_size_x))) > 0.4:
                    vrx = vrx + 1
            if ((wall_list[i][1]/(maze.tile_size_y)) - int(wall_list[i][1]/(maze.tile_size_y))) > 0.4:
                    vry = vry + 1
            print("Wall", i)
            if wall_list[i] == col_point:
                print("Collision Wall")
                self.position_wall_col_x = vrx1
                self.position_wall_col_y = vry1
            else:
                 self.wall_list_x.append(vrx)
                 self.wall_list_y.append(vry)

            print("Position wall x:", vrx)
            print("Position wall y:", vry)

        # Valeur importante pour les rules
        position_joueur_x = self.position_joueur_grille[1]
        if(position_joueur_x == 0):
             position_joueur_x = 1
        position_joueur_y = self.position_joueur_grille[0]
        # Permet de savoir si le mur est a droite ou a gauche du joueur (negatif = a gauche et positif = a droite)
        self.pos_wall_player_x = self.position_wall_col_x - position_joueur_x
        print("Valeur joueur pas rapport mur x:", self.pos_wall_player_x)
        # Permet de savoir si le mur est en haut ou en bas du joueur (negatif = en bas et positif = en haut)
        self.pos_wall_player_y = self.position_wall_col_y - position_joueur_y
        print("Valeur joueur pas rapport mur y:", self.pos_wall_player_y)
        # Position des murs pres du joueur
        gauche = 0
        droite = 0
        haut = 0
        bas = 0
        
        
        


        deplacement = ['LEFT','DOWN','RIGHT','UP']
        #trouver un moyen de mettre a jour ces valeurs automatiquement
        N = 24
        M = 16

        # def set_M_N(M1,N1):
        #     global M,N
        #     M = M1
        #     N = N1

        # tile_size_x = PLAYER_SIZE*WIDTH/M #10,875
        # tile_size_y = PLAYER_SIZE*HEIGHT /N #4,75

        tile_size_x = 10.875
        tile_size_y = 4.75


        #distance to obstacle = player - 
        incoming_direction =  ctrl.Antecedent(np.arange(0, 4, 1), 'direction')
        distance_to_obstacle_x = ctrl.Antecedent(np.arange(-tile_size_x, tile_size_x , 1), 'distance_to_obstacle_x')
        distance_to_obstacle_y = ctrl.Antecedent(np.arange(-tile_size_y, tile_size_y , 1), 'distance_to_obstacle_y')
        direction = ctrl.Consequent(np.arange(0, 4, 1), 'direction')

        #c'est l'obstacle qui se trouve a _ par rapport au joueur
        incoming_direction.automf(4, names=['LEFT', 'DOWN', 'RIGHT', 'UP'])
        distance_to_obstacle_x.automf(3,names=['gauche','milieu','droite'])
        distance_to_obstacle_y.automf(3,names=['bas','milieu','haut']) 

        direction['LEFT'] = fuzz.trimf(direction.universe, [0, 0, 1])
        direction['DOWN'] = fuzz.trimf(direction.universe, [0, 1, 2])
        direction['RIGHT'] = fuzz.trimf(direction.universe, [1, 2, 3])
        direction['UP'] = fuzz.trimf(direction.universe, [2, 3, 3])



        # distance_to_obstacle_x.view()
        # distance_to_obstacle_y.view()
        # direction.view()

        # plt.show()


        # Rules
        rule1 = ctrl.Rule(distance_to_obstacle_x['gauche'] & distance_to_obstacle_y['bas'] & incoming_direction['UP'], direction['LEFT'])
        rule2 = ctrl.Rule(distance_to_obstacle_x['gauche'] & distance_to_obstacle_y['bas'] & incoming_direction['RIGHT'], direction['DOWN'])
        rule3 = ctrl.Rule(distance_to_obstacle_x['gauche'] & distance_to_obstacle_y['bas'] & incoming_direction['DOWN'], direction['DOWN'])
        rule4 = ctrl.Rule(distance_to_obstacle_x['gauche'] & distance_to_obstacle_y['bas'] & incoming_direction['LEFT'], direction['LEFT'])

        rule5 = ctrl.Rule(distance_to_obstacle_x['gauche'] & distance_to_obstacle_y['milieu'] & incoming_direction['UP'], direction['LEFT'])
        rule6 = ctrl.Rule(distance_to_obstacle_x['gauche'] & distance_to_obstacle_y['milieu'] & incoming_direction['RIGHT'], direction['UP']) #OU DOWN
        rule7 = ctrl.Rule(distance_to_obstacle_x['gauche'] & distance_to_obstacle_y['milieu'] & incoming_direction['DOWN'], direction['LEFT'])
        rule8 = ctrl.Rule(distance_to_obstacle_x['gauche'] & distance_to_obstacle_y['milieu'] & incoming_direction['LEFT'], direction['LEFT'])

        rule9 = ctrl.Rule(distance_to_obstacle_x['gauche'] & distance_to_obstacle_y['haut'] & incoming_direction['UP'], direction['UP'])
        rule10 = ctrl.Rule(distance_to_obstacle_x['gauche'] & distance_to_obstacle_y['haut'] & incoming_direction['RIGHT'], direction['UP'])
        rule11 = ctrl.Rule(distance_to_obstacle_x['gauche'] & distance_to_obstacle_y['haut'] & incoming_direction['DOWN'], direction['LEFT'])
        rule12 = ctrl.Rule(distance_to_obstacle_x['gauche'] & distance_to_obstacle_y['haut'] & incoming_direction['LEFT'], direction['LEFT'])

        rule13 = ctrl.Rule(distance_to_obstacle_x['milieu'] & distance_to_obstacle_y['bas'] & incoming_direction['UP'], direction['RIGHT']) #OU LEFT
        rule14 = ctrl.Rule(distance_to_obstacle_x['milieu'] & distance_to_obstacle_y['bas'] & incoming_direction['RIGHT'], direction['DOWN'])
        rule15 = ctrl.Rule(distance_to_obstacle_x['milieu'] & distance_to_obstacle_y['bas'] & incoming_direction['DOWN'], direction['UP'])
        rule16 = ctrl.Rule(distance_to_obstacle_x['milieu'] & distance_to_obstacle_y['bas'] & incoming_direction['LEFT'], direction['DOWN'])

        rule17 = ctrl.Rule(distance_to_obstacle_x['milieu'] & distance_to_obstacle_y['milieu'] & incoming_direction['UP'], direction['UP'])
        rule18 = ctrl.Rule(distance_to_obstacle_x['milieu'] & distance_to_obstacle_y['milieu'] & incoming_direction['RIGHT'], direction['RIGHT'])
        rule19 = ctrl.Rule(distance_to_obstacle_x['milieu'] & distance_to_obstacle_y['milieu'] & incoming_direction['DOWN'], direction['DOWN'])
        rule20 = ctrl.Rule(distance_to_obstacle_x['milieu'] & distance_to_obstacle_y['milieu'] & incoming_direction['LEFT'], direction['LEFT'])

        rule21 = ctrl.Rule(distance_to_obstacle_x['milieu'] & distance_to_obstacle_y['haut'] & incoming_direction['UP'], direction['UP']) 
        rule22 = ctrl.Rule(distance_to_obstacle_x['milieu'] & distance_to_obstacle_y['haut'] & incoming_direction['RIGHT'], direction['UP'])
        rule23 = ctrl.Rule(distance_to_obstacle_x['milieu'] & distance_to_obstacle_y['haut'] & incoming_direction['DOWN'], direction['DOWN']) #OU LEFT
        rule24 = ctrl.Rule(distance_to_obstacle_x['milieu'] & distance_to_obstacle_y['haut'] & incoming_direction['LEFT'], direction['UP'])

        rule25 = ctrl.Rule(distance_to_obstacle_x['droite'] & distance_to_obstacle_y['bas'] & incoming_direction['UP'], direction['RIGHT'])
        rule26 = ctrl.Rule(distance_to_obstacle_x['droite'] & distance_to_obstacle_y['bas'] & incoming_direction['RIGHT'], direction['RIGHT'])
        rule27 = ctrl.Rule(distance_to_obstacle_x['droite'] & distance_to_obstacle_y['bas'] & incoming_direction['DOWN'], direction['DOWN'])
        rule28 = ctrl.Rule(distance_to_obstacle_x['droite'] & distance_to_obstacle_y['bas'] & incoming_direction['LEFT'], direction['DOWN'])

        rule29 = ctrl.Rule(distance_to_obstacle_x['droite'] & distance_to_obstacle_y['milieu'] & incoming_direction['UP'], direction['RIGHT'])
        rule30 = ctrl.Rule(distance_to_obstacle_x['droite'] & distance_to_obstacle_y['milieu'] & incoming_direction['RIGHT'], direction['RIGHT'])
        rule31 = ctrl.Rule(distance_to_obstacle_x['droite'] & distance_to_obstacle_y['milieu'] & incoming_direction['DOWN'], direction['RIGHT'])
        rule32 = ctrl.Rule(distance_to_obstacle_x['droite'] & distance_to_obstacle_y['milieu'] & incoming_direction['LEFT'], direction['DOWN'])

        rule34 = ctrl.Rule(distance_to_obstacle_x['droite'] & distance_to_obstacle_y['haut'] & incoming_direction['RIGHT'], direction['RIGHT'])
        rule35 = ctrl.Rule(distance_to_obstacle_x['droite'] & distance_to_obstacle_y['haut'] & incoming_direction['DOWN'], direction['RIGHT'])
        
        direction_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, 
                                             rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, 
                                             rule24, rule25, rule26, rule27, rule28, rule29, rule30, rule31, rule32, rule34, rule35])

        direction_decision = ctrl.ControlSystemSimulation(direction_ctrl)

        # Function to decide direction
        def decide_direction(distance_x, distance_y, incoming_dir):
            direction_decision.input['distance_to_obstacle_x'] = distance_x
            direction_decision.input['distance_to_obstacle_y'] = distance_y
            direction_decision.input['direction'] = incoming_dir
            direction_decision.compute()
            return direction_decision.output['direction']

        #TODO normaliser les distance player-obstacle de sorte a avoir les valeurs entre -10 et 10
        # Example usage
        distance_x_value = self.position_joueur_x - self.position_wall_col_x  # Replace with actual value
        distance_y_value = self.position_joueur_y - self.position_wall_col_y  # Replace with actual value
        print("distance_x_value", distance_x_value)
        print("distance_y_value", distance_y_value)
        incoming_direction_value = 1  # Replace with actual value  ['LEFT','DOWN','RIGHT','UP']

        result = decide_direction(distance_x_value, distance_y_value, incoming_direction_value)
        if self.old_way == deplacement[round(result)]:
            if deplacement[round(result)] == 'DOWN':
                    self.compteur = self.compteur + 1
                    if self.compteur > 2:
                        deplacement[round(result)] = 'UP'
                        self.compteur = 0
            elif deplacement[round(result)] == 'UP':
                    self.compteur = self.compteur + 1
                    if self.compteur > 2:
                        deplacement[round(result)] = 'DOWN'
                        self.compteur = 0
            elif deplacement[round(result)] == 'RIGHT':
                    self.compteur = self.compteur + 1
                    if self.compteur > 2:
                        deplacement[round(result)] = 'LEFT'
                        self.compteur = 0
            elif deplacement[round(result)] == 'LEFT':
                    self.compteur = self.compteur + 1
                    if self.compteur > 2:
                        deplacement[round(result)] = 'RIGHT'
                        self.compteur = 0

        self.old_way = deplacement[round(result)]
        print("Direction decision:", deplacement[round(result)],' ',result)
        ia.ajoutParcours(str(deplacement[round(result)]), player, self.compteur)