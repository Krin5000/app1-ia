from Player import *
from Maze import *
from swiplserver import PrologMQI

class DoorsOpen:
    def __init__(self, maze, player):
        self.maze = maze
        self.player = player
        self.nbCristaux = 0
        self.couleur_serrure = ''

    def solveDoor(self, _display_surf):
        door_state = self.maze.look_at_door(self.player, _display_surf)

        print("Etat de la porte:", door_state)

        key = ''

        self.nbCristaux = 0

        cristaux = []

        self.cristaux_rouge = 0
        self.cristaux_bleu = 0
        self.position_cristal_bleu = 0
        self.position_cristal_rouge = 0
        self.cristaux_jaune = 0
        self.cristaux_noir = 0
        self.cristaux_blanc = 0
        door = []

        for j in range(len(door_state[0])):
            if door_state[0][j] != '' and self.nbCristaux != 0:
                cristaux.append(door_state[0][j])
            if door_state[0][j] != '':
                self.nbCristaux = self.nbCristaux + 1
                door.append(door_state[0][j])
            if j == 0:
                self.couleur_serrure = door_state[0][j]
        self.nbCristaux = self.nbCristaux - 1

        print("Door:", door)

        with PrologMQI() as mqi_file:
            with mqi_file.create_thread() as prolog_thread:
                # Find the key for 3 cristaux
                if self.nbCristaux == 3:
                    # Load a prolog file
                    result = prolog_thread.query("[prolog/cristaux_3].")
                    print(result)
                    # Query the information in the file
                    result = prolog_thread.query("unlock_door_3("+ str(door) +", Position).")
                    print(result[0]['Position'])
                    key = result[0]['Position']
                
                # Find the key for 4 cristaux
                if self.nbCristaux == 4:
                    # Load a prolog file
                    result = prolog_thread.query("[prolog/cristaux_4].")
                    print(result)
                    # Query the information in the file
                    result = prolog_thread.query("unlock_door_4(" + str(door) + ", Position).")
                    print(result[0]['Position'])
                    key = result[0]['Position']

                # Find the key for 5 cristaux
                if self.nbCristaux == 5:
                    # Load a prolog file
                    result = prolog_thread.query("[prolog/cristaux_5].")
                    print(result)
                    # Query the information in the file
                    result = prolog_thread.query(
                        "unlock_door_5(" + str(door) + ", Position).")
                    print(result[0]['Position'])
                    key = result[0]['Position']
                
                # Find the key for 6 cristaux
                if self.nbCristaux == 6:
                    # Load a prolog file
                    result = prolog_thread.query("[prolog/cristaux_6].")
                    print(result)
                    # Query the information in the file
                    result = prolog_thread.query(
                        "unlock_door_6(" + str(door) + ", Position).")
                    print(result[0]['Position'])
                    key = result[0]['Position']

        print("Key = ", key)

        self.maze.unlock_door(key)