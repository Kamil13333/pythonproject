import pygame



class Player:
    def __init__(self,name):
        self.name=name


class Chamber:
    def __init__(self,id):
        self.id=id


    def show_chamber(self):
        pygame.display.set_mode((800, 600))


class Underworld:
    def __init__(self):
        self.list_of_chambers={} # key id of chamber values Chamber members
    def add_a_chamber(self,id):
        new_chamber=Chamber(id)
        self.list_of_chambers[id]=new_chamber
    def start_game(self):
        pygame.init()
        Chamber(1).show_chamber()
        #pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Underworld")


        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def end_game(self):
        pass
Underworld().start_game()
