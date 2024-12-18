import pygame
from random import choice
import time
import numpy as np

class Cell(pygame.sprite.Sprite):
    def __init__(self, loc):
        super().__init__()
        
        #create image and rectangle
        self.image = pygame.Surface((cell_size,cell_size)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(loc))

        #establish relative location in the 2d numpy array
        self.relative_location = (int(loc[0] / cell_size), int(loc[1] / cell_size))

        #random chance at the start of the game to be dead or alive
        self.is_alive = choice((True, False, False, False,False,False))
        self.fill_color()

        #establish instance variables for class, arbitrary for now
        self.neighbors = []
        self.next_state = None

    #runs once after all cells are created and establishes a cell's neighbors
    def get_neighbors(self):
        for i in range(-1,2):
            for j in range(-1,2):
                if not(i == 0 and j == 0):
                    new_i = (self.relative_location[0] + i) % game_w
                    new_j = (self.relative_location[1] + j) % game_h
                    if cell_array[new_i, new_j]:
                        self.neighbors.append(cell_array[new_i, new_j])

    #enforces the rules of Conway's game of life
    def check(self):
        living_neighbors = [x for x in self.neighbors if x.is_alive]

        if not self.is_alive:
            if len(living_neighbors) == 3:
                self.next_state = True

        if self.is_alive:
            if len(living_neighbors) < 2:
                self.next_state = False           
            if len(living_neighbors) > 3:
                self.next_state = False
            # else:
            #     #do something

    #sets cells to their next state
    def update_states(self):
        self.is_alive = self.next_state
        self.fill_color() #very important!! fills the color after the new generation is determined


    #method to fill the image with White for living cells, Black for dead cells
    def fill_color(self):
        if self.is_alive:
            self.image.fill('White')
        else:
            self.image.fill('Black')

    def clear(self):
        self.next_state = False
        self.update_states()

    def spawn(self):
        self.next_state = True
        self.update_states()

    #update from group Sprite class
    def update(self, selection):
        if selection == 'check':
            self.check()
        elif selection == 'update_states':
            self.update_states()
        elif selection == 'clear':
            self.clear()

class Text(pygame.sprite.Sprite):
    def __init__(self, font_size, text, color, center_pos):
        super().__init__()
        self.font = pygame.font.Font('PyGameTest/Assets/font/Pixeltype.ttf', font_size)
        self.image = self.font.render(text, False, color)
        self.rect = self.image.get_rect(center=(center_pos))

    def update():
        return
    
class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 1, 1)

#method for setting the width and height of the main screen
def set_screen(w, h):
    global screen, screen_w, screen_h, game_w, game_h, cell_size
    screen = pygame.display.set_mode((w + 200,h))
    screen_w = w
    screen_h = h

pygame.init()
pygame.display.init()

clock = pygame.time.Clock()

set_screen(800,800)

cell_size = 10

#initialize the sounds
beep_sound = pygame.mixer.Sound(rf'SallysGameOfLife/assets/sounds/beep.mp3')
beep_sound.play()


#values for computations late
game_w = int(screen_w / cell_size)
game_h = int(screen_h / cell_size)

#group for Cell class
cell_group = pygame.sprite.Group()

#array stores Cells and allows for easy access
cell_array = np.zeros((game_w, game_h), Cell)

#populate array
for i in range(game_w):
    for j in range(game_h):
        new_cell = Cell((i * cell_size, j * cell_size))
        cell_array[i, j] = new_cell
        cell_group.add(new_cell)

#establish each cell's neighborss
for cell in cell_group:
    cell.get_neighbors()
        

#custom timer, generation cycles each tick
cell_timer = pygame.USEREVENT + 1
pygame.time.set_timer(cell_timer, 100)

game_state = 'running'

menu_surf = pygame.Surface((200,800))
menu_rect = menu_surf.get_rect(topleft=(800,0))

#add all game text
text_group = pygame.sprite.Group()
text_group.add(Text(50, 'Menu', 'White', (900, 40)))
clear_text = Text(25, 'Clear', 'White', (850, 80))
text_group.add(clear_text)

while True:
    #main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    break

        if event.type == pygame.MOUSEBUTTONDOWN:
            #if player clicks 'clear' button
            if clear_text.rect.collidepoint(pygame.mouse.get_pos()):
                cell_group.update('clear')


        if game_state == 'running':  
            if event.type == cell_timer:                   
                cell_group.update('check') #check for cells living/dying and set their next state
                cell_group.update('update_states') #update all current states to next state

            if event.type == pygame.KEYDOWN:       
                if event.key == pygame.K_SPACE:
                    game_state = 'paused'            
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollide(Point(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), cell_group, False):
                    game_state = 'drawing'

                
        #mouse collisions with drawing is pretty bugged at the moment

        elif game_state == 'paused':            
            if event.type == pygame.KEYDOWN:       
                if event.key == pygame.K_SPACE:       
                    game_state = 'running'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollide(Point(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), cell_group, False):
                    game_state = 'drawing'
    
                
        elif game_state == 'drawing': 
            if event.type == pygame.MOUSEBUTTONUP:
                game_state = 'paused'
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = 'running'

            if pygame.mouse.get_pressed()[0]:
                cell_collisions = pygame.sprite.spritecollide(Point(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), cell_group, False)
                if cell_collisions:
                    for cell in cell_collisions:
                        cell.spawn()
            else:
                game_state = 'running'
        
                
    cell_group.draw(screen) #draw cells    
    text_group.draw(screen) #draw text

    #draw menu border
    pygame.draw.rect(screen, 'Red', menu_rect, cell_size)

    #necessary for pygame :/
    pygame.display.update()
    clock.tick(60)    