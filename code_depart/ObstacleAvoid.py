from Constants import *
from WayOut import *
import numpy as np
import FuzzyLogic as FL


class ObstacleAvoid:
    
    """Cette fonction prendra le chemin généré par WayOut
    puis récupère la position de l'obstacle et génère des instructions supplémentaires
    
    maze : l'objet maze instancié qui comporte les informations du labyrinthe
    wayout: l'objet contenant les informations sur le chemin de sortie
    player: l'objet instancié représentant le joueur
    
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
        """fonction qui va mettre à jour la position de l'obstacle
        """
        obstacle_list = self.maze.obstacleList
        indice = self.trouver_indice_plus_petite_distance(obstacle_list)
        self.obstacle_position = obstacle_list[indice]
    
            
        
        
    def trouver_indice_plus_petite_distance(self,L1):
        '''fonction qui permet de retrouver l'obstacle le plus proche en fonction 
        des coordonnées x et y puis retourne l'indice de l'obstacle le plus proche
        L1: liste d'obstacles en format rect[a,b,c,d]
            a,b les coordonnées du sommets
            c,d les dimensions 
        '''
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
        '''fonction qui va retourner la direction optimale à prendre pour éviter l'obstacle
        retourne l'indice de la direction suivant la liste ['LEFT','DOWN','RIGHT','UP']
        ou -1 si la direction n'existe pas.
        '''
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
        """fonction qui va mettre à jour le chemin de wayout afin d'intégrer les directions permettant
        l'évitement des obstacles. 

        Args:
            rectified_direction_id (int): l'indice de la direction suivant la liste ['LEFT','DOWN','RIGHT','UP']
            ia (IA): objet instancié représentant le joueur intelligent
        """
        deplacement = ['LEFT','DOWN','RIGHT','UP']
        rectified_direction = deplacement[rectified_direction_id]
        
        list_d = []
        obstacle_width = 0.2*self.tile_size_x   
        obstacle_heigth = 0.2*self.tile_size_y
        incr = round(min(obstacle_width,obstacle_heigth)) 
        wayout = ia.wayout
        
        list_d += [rectified_direction]*incr 
        nbrM = ia.nbrM
        deviation =wayout.indications_deplacement[:nbrM] + list_d + wayout.indications_deplacement[nbrM:]
        contrary_list = ['RIGHT','UP','LEFT','DOWN']
        
         
        contrary = contrary_list[rectified_direction_id]
        list_c = []
        list_c += [contrary]*incr
        
        wayout.indications_deplacement = deviation[:2*incr + nbrM] + list_c + deviation[2*incr + nbrM:]
        ia.nbrM = nbrM+1
        
        
        