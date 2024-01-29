from Constants import *
from WayOut import *
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import FuzzyLogic as FL


class ObstacleAvoid:
    
    """Cette fonction prendra le chemin généré par WayOut
    puis récupère la position de l'obstacle et génère un chemin alternatif (ou des instructions supplémentaires)
    et réécris la fonction de wayout en placant les instructions
    
    l'algorithme de logique flou va prendre en entrée la position du joueur et de l'obstacle et retourne un des chiffres
    0: tout a gauche
    1: un peu a gauche
    2: tout droit
    3: un peu a droite 
    4: tout a droite 
    
    puis on ajoute la nouvelle direction a la liste qu'on va réécrire
    """
    def __init__(self,maze,wayout,player):        
        self.maze = maze
        self.chemin = wayout
        self.obstacle_position = None
        self.player = player
        self.N = len(self.maze.maze)
        self.M = len(self.maze.maze[0])
        self.tile_size_x = WIDTH/self.M
        self.tile_size_y = HEIGHT / self.N
        
    
    def set_obstacle_position(self):
        obstacle_list = self.maze.obstacleList
        indice = self.trouver_indice_plus_petite_distance(obstacle_list)
        self.obstacle_position = obstacle_list[indice]
    
            
        
        
    def trouver_indice_plus_petite_distance(self,L1):
        x,y = self.player.get_position()
        if not L1:
            return None  # Retourne None si la liste est vide

        # Convertir la liste en tableau NumPy pour un traitement vectoriel
        points = np.array([[point[0], point[1]] for point in L1])

        # Calculer les distances selon l'axe x et l'axe y
        distances_x = np.abs(points[:, 0] - x)
        distances_y = np.abs(points[:, 1] - y)

        # Calculer la somme des distances selon les deux axes
        distances_totales = distances_x + distances_y

        # Trouver l'indice du point ayant la plus petite somme des distances
        indice_min_total = np.argmin(distances_totales)
        return indice_min_total
    
    def rectifier(self):
        deplacement = ['LEFT','DOWN','RIGHT','UP']
        x,y = self.player.get_position()
        obs_x,obs_y = self.obstacle_position[0],self.obstacle_position[1]
        
        #distance to obstacle = player - obstacle (dans un repère classique en ramenant au repère pygame x=x et y=-y)
        distance_to_obstacle_x = x - obs_x
        distance_to_obstacle_y = obs_y - y
        
        print('distance x ', distance_to_obstacle_x)
        print('distance y ', distance_to_obstacle_y)
        
        if self.chemin in deplacement:
            indice_de_direction = np.where(np.array(deplacement) == self.chemin)[0].tolist()
            rectified_direction = FL.decide_direction(distance_to_obstacle_x,distance_to_obstacle_y,indice_de_direction)
            return rectified_direction
        else:
            print(self.chemin, "n'est pas dans la liste deplacement.")
            return -1
        
    
    def rectified_list(self,rectified_direction_id,ia):
        deplacement = ['LEFT','DOWN','RIGHT','UP']
        rectified_direction = deplacement[rectified_direction_id]
        
        list_d = []
        obstacle_width = ITEM_SIZE*self.tile_size_x   
        obstacle_heigth = ITEM_SIZE*self.tile_size_y
        incr = round(min(obstacle_width,obstacle_heigth))
        wayout = ia.wayout
        
        list_d += [rectified_direction]*incr 
        nbrM = ia.nbrM
        # print('avant rectification: ' , wayout.indications_deplacement)
        deviation =wayout.indications_deplacement[:nbrM] + list_d + wayout.indications_deplacement[nbrM:]
        # print('après deviation: ' , deviation)
        contrary_list = ['RIGHT','UP','LEFT','DOWN']
        
         
        contrary = contrary_list[rectified_direction_id]
        list_c = []
        list_c += [contrary]*incr
        
        wayout.indications_deplacement = deviation[:2*incr + nbrM] + list_c + deviation[2*incr + nbrM:]
        ia.nbrM = nbrM+1
        # print('après rectification: ' , wayout.indications_deplacement)
        
    
    def NewWay(self,deplacement_id,ia):

        deplacement = ['LEFT','DOWN','RIGHT','UP']    
        ia.wayout.indications_deplacement.clear()
        # ia.wayout.profondeur_abord(self.player.get_position(), [deplacement[deplacement_id]])
        ia.wayout.indications_deplacement.extend(deplacement[deplacement_id])
        
        

        # chemin_solution = ia.wayout.profondeur_abord(self.player.get_position(), [deplacement[deplacement_id]])

        # for i in range(1, len(chemin_solution)):
        #     directions = ia.wayout.convertir_direction(
        #         chemin_solution[i - 1], chemin_solution[i], ia.wayout.distance_max
        #     )
        #     ia.wayout.indications_deplacement.extend(directions)
        print('new way :',deplacement[deplacement_id])
        