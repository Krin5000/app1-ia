from DefeatEnnemies import *
from DoorsOpen import *
from ObstacleAvoid import *
from TakeTokens import *
from TakeTreasures import *
from WayOut import *
from Constants import *

class IA:
    def __init__(self, maze, player):
        self.wayout = WayOut(maze, player)
        self.instruction = []
        self.nbrM = 0
        self.env = ''
        self.pl = player
        self.map = maze
        self.item_list_old = []
        self.changement = False
        


    def mouvement(self):
        #print("Grille:", self.wayout.return_way())
        #print("Position joueur:", self.pl.get_position())
        if self.nbrM < len(self.wayout.return_way()):
            self.env = self.wayout.return_way()[self.nbrM]
            self.nbrM = self.nbrM + 1
        #if self.nbrM < len(self.instruction):
        #    self.env = self.instruction[self.nbrM]
        #    self.nbrM = self.nbrM + 1
        else:
            self.env = ''
            if self.changement == True:
                self.nbrM = self.wayout.restart(self.pl)
                self.changement = False
        return self.env
    
    def verification_proxi(self, _display_surf):
        self.direction = []
        wall_list, obstacle_list, item_list, monster_list, door_list = self.map.make_perception_list(self.pl, _display_surf)
        if item_list != [] and self.item_list_old != item_list:
            print("Objets dans item_liste:", item_list)
            print("Position y:", item_list[0][1])
            print("Position x:", item_list[0][0])
            self.item_list_old = item_list
            self.changement = True
            self.nbrM = self.wayout.reenitialisation(self.pl, self.map, item_list, self.nbrM)
        
