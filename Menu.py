import pygame
import math
import random

def draw_text(text, font, color, x, y):
    textobj = font.render(text, 1, pygame.Color(color))
    textrect = textobj.get_rect()
    textrect.center = (x,y)
    surf.blit(textobj,textrect)

def button(text):
    return ((text,police[1],"#0099FF"), (text,police[2],"#FF5000"))

def menus(menu, selector, side_selector):
    if menu == "Space":
        if selector == 0:
            return solo_menu.run()
        elif selector == 1:
            return multi_menu.run()
        elif selector == 2:
            return options_menu.run()
        else:
            return False

    elif menu == "Solo":
        if selector == 0:
            print("Play solo")
            return True
        else:
            return "exit"

    elif menu == "Multi":
        if selector == 0:
            return multiGame()
        else:
            return "exit"

    elif menu == "Options":
        if selector == 0:
            global screen, screen_x, screen_y, surf
            screen = (screen + 1)%len(screens)
            screen_x = screens[screen][0]
            screen_y = screens[screen][1]
            surf = pygame.display.set_mode((screen_x, screen_y))
            options_menu.buttons[0] = button("Screen "+str(screens[screen]))
            return True
        elif selector == 1:
            return keys_menu.run()
        else:
            return "exit"

    elif menu == "Keys":
        global keys
        global keys_innit
        if selector == 0:
            run = True
            while run :
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        keys[0][side_selector] = event.key
                        keys_menu.buttons[selector][side_selector] = button(pygame.key.name(event.key))
                        run = False
            return True
        elif selector == 1:
            run = True
            while run :
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        keys[1][side_selector] = event.key
                        keys_menu.buttons[selector][side_selector] = button(pygame.key.name(event.key))

                        run = False
            return True
        elif selector == 2:
            print(keys[1])
            print(keys_menu.buttons[1])
            keys = keys_innit
            keys_menu.buttons[0] = [button(pygame.key.name(i)) for i in keys[0]]
            keys_menu.buttons[1] = [button(pygame.key.name(i)) for i in keys[1]]
            print(keys[1])
            print(keys_menu.buttons[1])
            return True
        else:
            return "exit"

    elif menu == "Pause":
        if selector == 0:
            return "exit"
        elif selector == 1:
            return options_menu.run()
        elif selector == 2:
            return "restart"
        else:
            return False

class Menu:

    def __init__(self, title, buttons):
        self.title = title
        self.buttons = []
        self.side_buttons = []
        self.Nbr_buttons = len(buttons)

        for i in range(self.Nbr_buttons):
            if type(buttons[i]) == list:
                self.buttons.append([])
                self.side_buttons.append(True)
                for l in buttons[i]:
                    self.buttons[i].append(button(l))
            else:
                self.buttons.append(button(buttons[i]))
                self.side_buttons.append(False)

    def run(self):
        run = True
        selector = 0
        side_selector = 0
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selector = (selector-1)%self.Nbr_buttons
                        side_selector = 0

                    if event.key == pygame.K_DOWN:
                        selector = (selector+1)%self.Nbr_buttons
                        side_selector = 0

                    if event.key == pygame.K_RIGHT:
                        if self.side_buttons[selector]:
                            side_selector = (side_selector+1)%len(self.buttons[selector])

                    if event.key == pygame.K_LEFT:
                        if self.side_buttons[selector]:
                            side_selector = (side_selector-1)%len(self.buttons[selector])

                    if event.key == pygame.K_RETURN:
                        exit = menus(self.title,selector,side_selector)
                        if exit == "exit":
                            return True
                        elif exit == False:
                            return False
                        elif exit != True:
                            return exit

            surf.fill((15,15,40))
            draw_text(self.title, police[0], "#FF5000", screen_x/2, screen_y/4)

            for i in range(self.Nbr_buttons):
                if i == selector:
                    if self.side_buttons[i]:
                        text = self.buttons[i][side_selector][1]
                    else:
                        text = self.buttons[i][1]
                    draw_text(text[0],text[1],text[2], screen_x/2, screen_y/4+pos[i])
                else:
                    if self.side_buttons[i]:
                        text = self.buttons[i][0][0]
                    else:
                        text = self.buttons[i][0]
                    draw_text(text[0],text[1],text[2], screen_x/2, screen_y/4+pos[i])
            pygame.display.flip()
        return run

def multiGame():
    game = True

    # Importation des images de tir et des vaisseau de chaque couleur
    tir_blue = pygame.image.load("tir_blue.png").convert_alpha()
    tir_blue = pygame.transform.scale(tir_blue,(10,30))
    tir_red = pygame.image.load("tir_red.png").convert_alpha()
    tir_red = pygame.transform.scale(tir_red,(10,30))

    ship_red = pygame.image.load("ship_red.png").convert_alpha()
    ship_red_forward = pygame.image.load("ship_red_forward.png").convert_alpha()
    ship_blue = pygame.image.load("ship_blue.png").convert_alpha()
    ship_blue_forward = pygame.image.load("ship_blue_forward.png").convert_alpha()

    vie_red = pygame.image.load("vie_red.png").convert_alpha()
    vie_red = pygame.transform.scale(vie_red,(10,30))
    vie_blue = pygame.image.load("vie_blue.png").convert_alpha()
    vie_blue = pygame.transform.scale(vie_blue,(10,30))

    # Initialisation de la classe Ship, avec les fonctions par vaisseau
    class Ship:

        def __init__(self, x, y, angle, pt_vie, ship_img, ship_forward_img, tir_img, vie_img, key):
            self.x = x
            self.y = y
            self.a = angle
            self.v = 0
            self.pv = pt_vie
            self.act = self.img = pygame.transform.scale(ship_img,(76,76))
            self.img_forward = pygame.transform.scale(ship_forward_img,(76,76))
            self.rect = self.img.get_rect(center=(self.x,self.y))
            self.tir_img = tir_img
            self.vie_img = vie_img
            self.tirs = []
            self.key = key
            self.degats = 0

        def move(self):
            keys_actual = pygame.key.get_pressed()
            img = self.img

            if keys_actual[self.key[2]]:
                img = self.img_forward
                if self.v<700:
                    self.v += 20
            else:
                if self.v>0:
                    self.v -= 5

            if keys_actual[self.key[3]]:
                if self.v>0:
                    self.v -= 20
                elif self.v>-300:
                    self.v -= 5
            else:
                if self.v<0:
                    self.v += 5

            if keys_actual[self.key[0]]:
                x = math.sqrt((self.v / fps)**2)+5
                if x < 10:
                    x = 5
                self.a = (self.a-50/x)%360

            if keys_actual[self.key[1]]:
                x = math.sqrt((self.v / fps)**2)+5
                if x < 10:
                    x = 6
                self.a = (self.a+50/x)%360

            if keys_actual[self.key[4]]:
                self.tir()

            self.act = pygame.transform.rotate(img,self.a)
            rad = math.radians(self.a)
            self.x = (self.x-(self.v//fps)*math.sin(rad))%screen_x
            self.y = (self.y-(self.v//fps)*math.cos(rad))%screen_y
            self.rect = self.act.get_rect(center=(self.x,self.y))

        def tir(self):
            if self.tirs == []:
                self.tirs.append([self.x, self.y, self.a, 25, 0])
            elif self.tirs[-1][4] > 10:
                self.tirs.append([self.x, self.y, self.a, 25, 0])

        def touch(self):
            self.pv -= 1
            self.degats = 60
            if self.pv == 0:
                return False
            else:
                return True

        def update(self, enemy):
            r = True
            p = []
            for i in range(0,len(self.tirs)):
                if self.tirs[i][4]<self.tirs[i][3]:
                    tir_act = pygame.transform.rotate(self.tir_img,self.tirs[i][2])
                    surf.blit(tir_act,(self.tirs[i][0],self.tirs[i][1]))
                    rad = math.radians(self.tirs[i][2])
                    self.tirs[i][0] = (self.tirs[i][0]-self.tirs[i][3]*math.sin(rad))%screen_x
                    self.tirs[i][1] = (self.tirs[i][1]-self.tirs[i][3]*math.cos(rad))%screen_y
                    self.tirs[i][4] += 1
                else:
                    p.append(i)
                if self.tirs[i][0]-25 < enemy.x < self.tirs[i][0]+25 and self.tirs[i][1]-25 < enemy.y < self.tirs[i][1]+25 :
                    r = enemy.touch()
                    if i not in p:
                        p.append(i)
            for i in p:
                self.tirs.pop(i)
            if (self.degats//10)%2 == 0 :
                surf.blit(self.act,self.rect)
            if self.degats > 0:
                self.degats -= 1
            return r

        def __del__(self):
            pass

    ship1=Ship(screen_x/4, screen_y/2, 0, 3, ship_blue, ship_blue_forward, tir_blue, vie_blue, keys[0])
    ship2=Ship(screen_x*3/4, screen_y/2, 0, 3, ship_red, ship_red_forward, tir_red, vie_red, keys[1])

    #Boucle de jeu
    while game :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit = pause_menu.run()
                    if exit == 'restart':
                        del ship1
                        del ship2
                        ship1=Ship(screen_x/4, screen_y/2, 0, 3, ship_blue, ship_blue_forward, tir_blue, vie_blue, keys[0])
                        ship2=Ship(screen_x*3/4, screen_y/2, 0, 3, ship_red, ship_red_forward, tir_red, vie_red, keys[1])
                    elif not exit:
                        return True

                if event.key == pygame.K_BACKSPACE:
                    del ship1
                    del ship2
                    ship1=Ship(screen_x/4, screen_y/2, 0, 3, ship_blue, ship_blue_forward, tir_blue, vie_blue, keys[0])
                    ship2=Ship(screen_x*3/4, screen_y/2, 0, 3, ship_red, ship_blue_forward, tir_red, vie_red, keys[1])

        ship1.move()
        ship2.move()

        surf.fill((15,15,40))
        game = ship1.update(ship2)
        if not game:
            gameOver('red')
        else:
            game = ship2.update(ship1)
            if not game:
                gameOver('blue')

        x_vie = (screen_x/4)-20
        for i in range(ship1.pv):
            surf.blit(ship1.vie_img,(x_vie,30))
            x_vie += 20
        x_vie = (screen_x*3/4)-20
        for i in range(ship2.pv):
            surf.blit(ship2.vie_img,(x_vie,30))
            x_vie += 20

        pygame.display.flip()
        clock.tick(fps)
    return True

def gameOver(team):
    run  = True
    compteur = 0
    if team == 'red':
        color = colors[0]
    elif team == 'blue':
        color = colors[1]
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True

        compteur = (compteur+1)%30
        surf.fill((15,15,40))
        draw_text("Game Over",police[0],color,screen_x/2, screen_y/2)
        if compteur<15:
            draw_text("Press Enter", police[1], color, screen_x/2, screen_y/2+50)
        pygame.display.flip()
        clock.tick(fps)

# Valeurs pour réglages écran
screen = 1
screens = [(600,400),(800,600),(1300,700)]
screen_x = screens[screen][0]
screen_y = screens[screen][1]
fps = 30
pos = [100, 150, 200, 250, 300, 350]

# Création de la fenêtre de jeu
surf = pygame.display.set_mode((screen_x,screen_y))
surf.fill((15,15,40))
clock=pygame.time.Clock()
pygame.key.set_repeat(300,400)

# Initialisation des polices de caractère
pygame.font.init()
police = []
police.append(pygame.font.Font("Retro Gaming.ttf",80))
police.append(pygame.font.Font("Retro Gaming.ttf",30))
police.append(pygame.font.Font("Retro Gaming.ttf",35))

# Valeurs utilisées couramment
keys_innit = [[pygame.K_d,pygame.K_a,pygame.K_w,pygame.K_s,pygame.K_SPACE],[pygame.K_RIGHT,pygame.K_LEFT,pygame.K_UP,pygame.K_DOWN,pygame.K_RSHIFT]]
keys = [[pygame.K_d,pygame.K_a,pygame.K_w,pygame.K_s,pygame.K_SPACE],[pygame.K_RIGHT,pygame.K_LEFT,pygame.K_UP,pygame.K_DOWN,pygame.K_RSHIFT]]
default_keys = keys
colors = ["#FF5000","#0099FF"]

# Création des menus
main_menu = Menu("Space", ["Solo", "Multi", "Options", "Quit"])
solo_menu = Menu("Solo", ["Play", "Exit"])
multi_menu = Menu("Multi", ["Play", "Exit"])
options_menu = Menu("Options", ["Screen "+str(screens[screen]), "Keys", "Exit"])
keys_menu = Menu("Keys", [[pygame.key.name(i) for i in keys[0]], [pygame.key.name(i) for i in keys[1]], "Réinitialiser", "Exit"])
pause_menu = Menu("Pause", ["Return", "Options", "Restart", "Exit"])

# Lancement du programme
main_menu.run()
print('clean quit')
pygame.quit()
