import pygame
import random


#  Moim  głównym źródłem z którego korzystałem jeśli chodzi o zastosowanie  biblioteki pygame jest
#  https://github.com/attreyabhatt/Space-Invaders-Pygame/blob/master/main.py


# Tworzę okno gry wraz z graficznym tłem
pygame.init()
window = pygame.display.set_mode((900, 600))
background = pygame.image.load('background.png')
wall = pygame.image.load('wall.jpg')

pygame.display.set_caption("Underworld")
# Funkcja is_impact odpowiada za wykrywanie kolizji między obiektami
def is_impact( x1, y1, x2, y2):
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1 / 2)
    if distance <= 40:
        return True
    else:
        return False

class Key():
    '''
    Klasa Key reprezentuje klucz który służy do otwierania skarbów
    '''
    def __init__(self,id,x=200,y=400,image=pygame.image.load('key.png'),free=True):
        self.id=id
        self.image = image
        self.x = x
        self.y = y
        self.free=free

    def show_the_key(self):

        window.blit(self.image, (self.x, self.y))

class Treasure:
    '''Klasa Treasure reprezentuje skarb, który może zostać zdobyty przez gracza'''
    def __init__(self,x=600,y=200,image=pygame.image.load('treasure.png'),opened=False):

        self.image = image
        self.x = x
        self.y = y
        # Dodaję do zawartości skarbu losową liczbę złota i diamentów z przedziału od 1 do 10
        self.contents=dict()
        self.contents['gold']=random.randint(1,10)
        self.contents['diamond'] = random.randint(1, 10)
        self.opened=opened
    def show_the_treasure(self):
        window.blit(self.image, (self.x, self.y))





class Gate:
    '''Klasa Gate reprezentuje bramę dzięki której można przejść na kolejny poziom'''
    def __init__(self,id,x=750,y=0,image=pygame.image.load('gate.png')):
        self.id=id
        self.image=image
        self.x=x
        self.y=y

    def show_the_gate(self):
        window.blit(self.image, (self.x, self.y))


class Player:
    '''Klasa Player reprezentuje gracza'''
    def __init__(self,bag={'treasure_key' : 0, 'gold':0,'diamond':0},name='Jane',game_active=True,image=pygame.image.load('action-figure.png'),x=100,y=500,whichchamber=1):
        self.name=name
        self.image=image
        self.x=x
        self.y=y
        self.bag=bag
        self.game_active=game_active

        self.whichchamber=whichchamber

    def show_player(self):
        window.blit(self.image,(self.x,self.y))
    def move_player(self,direction):
        # Jeśli gra jest aktywna to gracz porusza się zgodnie z naciskanymi klawiszami
        if self.game_active == True:
            if direction=='right':
                self.x+=1
            elif direction=='left':
                self.x-= 1
            elif direction=='up':
                self.y-= 1
            elif direction=='down':
                self.y+= 1

    def merge_bags(self,bag,store2):
        # Dodaje do torby gracza zdobyty skarb
        sumstore=bag.copy()
        for key1 in bag:
            for key2 in store2:
                if key1==key2:
                    sumstore[key1]=bag[key1]+store2[key2]
        for key2 in store2:
            if key2 not in sumstore:
                sumstore[key2]=store2[key2]
        self.bag=sumstore

class Creature:
    '''Klasa Creature reprezentuje stwora który goni gracza ay zarać mu zdobyte skarby'''
    def __init__(self,x=600,y=400,image=pygame.image.load('mythical-creature.png'),game_active=True):
        self.image = image
        self.x = x
        self.y = y
        self.game_active=game_active
    def show_the_creature(self):
        window.blit(self.image, (self.x, self.y))
    def move_the_creature(self,Jane=Player()):
        if self.game_active==True:

            if Jane.x>=self.x and Jane.y>=self.y:
                self.x+=0.5
                self.y+=0.5
            elif Jane.x<self.x and Jane.y>self.y:
                self.x-= 0.5
                self.y+=0.5
            elif Jane.x<=self.x and Jane.y<=self.y:
                self.y-= 0.5
                self.x -=0.5
            elif Jane.x>self.x and Jane.y<self.y:
                self.y-= 0.5
                self.x+=0.5

class Chamber:
    '''Klasa Chamber reprezentuje komnatę '''
    def __init__(self,id=1):
        self.id=id

    def playing_in_first_chamber(self,Jane=Player(),  Heffalump = Creature()):

        # Gracz oraz stwór nie mogą znajdować się tam gdzie stoi mur
        if Jane.x ==351 and Jane.y >=200:
            Jane.x =350
        if Jane.x == 449 and Jane.y>=200:
            Jane.x = 450
        if Jane.x>=350 and Jane.x<=430 and Jane.y==201:
            Jane.y=200
        if Heffalump.x ==351 and Heffalump.y >=200:
            Heffalump.x =350
        if Heffalump.x == 449 and Heffalump.y>=200:
            Heffalump.x = 450
        if Heffalump.x>=350 and Heffalump.x<=430 and Heffalump.y==201:
            Heffalump.y=200
        # Gracz teleportuje sie do drugiej komnaty
        if Jane.x>=750 and Jane.y<=100:
            Jane.whichchamber=2



    def playing_in_chamber(self,Jane=Player(),Gate2 = Gate(2),  Heffalump = Creature(),Treasure2 = Treasure(),key2=Key(2)):
        #Pokazuję na planszy wszsytkie potrzene obiekty
        Jane.show_player()
        Gate2.show_the_gate()
        Heffalump.show_the_creature()
        Treasure2.show_the_treasure()

        Heffalump.move_the_creature(Jane)
        #Jeśli klucz jest jeszcze do zdoycia i gracz podszedł do klucza to dodajemy klucz do torby gracza
        if key2.free == True:
            if is_impact(Jane.x, Jane.y, key2.x, key2.y) == False:
                key2.show_the_key()
            if is_impact(Jane.x, Jane.y, key2.x, key2.y) == True :
                Jane.bag['treasure_key'] += 1
                key2.free = False
        # pokazujemy skarb na planszy
        if is_impact(Jane.x, Jane.y, Treasure2.x, Treasure2.y) == False and Treasure2.opened == False:
            Treasure2.show_the_treasure()
            # gracz zdoywa skarb i zmieniamy graficzny obraz skarbu
        elif is_impact(Jane.x, Jane.y, Treasure2.x,
                       Treasure2.y) == True and Treasure2.opened == False and  Jane.bag['treasure_key']>0:
            Jane.bag['treasure_key']=Jane.bag['treasure_key']-1
            Jane.merge_bags(Jane.bag, Treasure2.contents)

            Treasure2.image = pygame.image.load('treasure_opened.png')
            Treasure2.opened = True
            Treasure2.show_the_treasure()

class Underworld:
    '''Klasa Underworld reprezentuje podziemia'''
    def __init__(self,game_active=True):

        self.game_active=game_active

    def start_game(self):
        # Rozpoczyna się gra
        self.game_active=True
        # Tworzę wszystkie oiekty których będę używał w trakcie gry

        Chamber_play=Chamber()


        Gate1 = Gate(1)
        Gate2=Gate(id=2,x=0,y=0)
        Gate3=Gate(id=3,x=750,y=450)
        Gate4 = Gate(id=4, x=300, y=180)

        Heffalump = Creature()
        Jane = Player()
        Treasure1 = Treasure()
        Treasure2=Treasure(x=800,y=500)
        Treasure3 = Treasure(x=0, y=500)
        Treasure4 = Treasure(x=800, y=0)
        key1 = Key(1)
        key2=Key(2,x=300,y=0)
        key3 = Key(3,x=500, y=200)
        key4 = Key(4,x=0, y=0)


        running = True
        while running:
            window.fill((0, 0, 0))
            window.blit(background,(0,0))
            # Obsługuję grę w pierwszej komnacie
            if Jane.whichchamber==1:
                window.blit(wall,(400,250))
                Chamber_play.playing_in_first_chamber(Jane,Heffalump)
                Chamber_play.playing_in_chamber(Jane, Gate1, Heffalump, Treasure1, key1)
                # Obsługuję grę w drugiej komnacie
            elif Jane.whichchamber==2:
                Chamber_play.playing_in_chamber(Jane,Gate2,Heffalump,Treasure2,key2)
                if Jane.x <= 100 and Jane.y <= 80:
                    Jane.whichchamber = 3
            # Obsługuję grę w trzeciej komnacie
            elif Jane.whichchamber==3:
                Chamber_play.playing_in_chamber(Jane,Gate3,Heffalump,Treasure3,key3)
                if Jane.x >= 750 and Jane.y >= 450:
                    Jane.whichchamber = 4
            # Obsługuję grę w czwartej komnacie
            elif Jane.whichchamber==4:
                Chamber_play.playing_in_chamber(Jane,Gate4,Heffalump,Treasure4,key4)

            # Jeśli stwór dogoni gracza to zabiera mu skarb
            if is_impact(Jane.x,Jane.y,Heffalump.x,Heffalump.y):
                Jane.bag['treasure_key']=0
                Jane.bag['gold']=0
                Jane.bag['diamond']=0





            for event in pygame.event.get():
                # Obsługuję wyjście z gry
                if event.type == pygame.QUIT:
                    running = False
                    # Po kliknięciu w ekran gry gdy gra jest zakończona mozna rozpocząć rozgrywkę od nowa
                    # Aby to zrobić skorzystałem z https://stackoverflow.com/questions/31300690/how-to-get-pygame-button-to-register-only-one-click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.game_active==False:
                        Jane.bag['treasure_key']=0
                        Jane.game_active=True

                        self.start_game()

# Dodaję obsługę poruszania gracza za pomocą strzałek
#Skorzystałem z https://stackoverflow.com/questions/60589873/why-does-this-code-work-outside-of-the-main-loop-in-pygame
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                Jane.move_player('left')

            elif keys[pygame.K_RIGHT]:
                Jane.move_player('right')
            elif keys[pygame.K_UP]:
                Jane.move_player('up')
            elif keys[pygame.K_DOWN]:
                Jane.move_player('down')

            # Dodaję granicę okna dla gracza ay nie wyskakiwał poza obręb planszy
            if Jane.x<=0:
                Jane.x=0
            elif Jane.x>=836:
                Jane.x=836
            if Jane.y<=0:
                Jane.y=0
            elif Jane.y>=536:
                Jane.y=536
            # Kończę grę gdy gracz jest w bramie czwartej komnaty
            if 300<= Jane.x<=400 and 180<=Jane.y<=250 and Jane.whichchamber==4:
                Heffalump.game_active = False
                Jane.game_active = False

                self.end_game()
            # Tworząc napisy do wyświetlania na ekranie skorzystałem z https://github.com/attreyabhatt/Space-Invaders-Pygame/blob/master/main.py
            font = pygame.font.Font('freesansbold.ttf', 16)
            game_over_font1 = pygame.font.Font('freesansbold.ttf', 48)


            score = font.render(("klucze : " + str(Jane.bag['treasure_key'])+"złoto : " + str( Jane.bag['gold']) + "diamenty : " + str(Jane.bag['diamond']) ), True, (255, 255, 255))
            window.blit(score, (0, 550))
            if Jane.game_active==False:
                recieved = game_over_font1.render(
                    "Zdobyte  złoto : " + str(Jane.bag['gold']) + " diamenty: " + str(Jane.bag['diamond']), True,
                    (255, 255, 255))
                window.blit(recieved, (100, 350))


            pygame.display.update()

    def end_game(self):
        # Wyświetlam napis kończący grę oraz zmieniam grę na nieaktywną
        game_over_font = pygame.font.Font('freesansbold.ttf', 64)
        game_over = game_over_font.render("Koniec gry!", True, (255, 255, 255))

        window.blit(game_over, (200, 250))

        self.game_active=False

if __name__ == "__main__":
    Underworld().start_game()
