import pygame
import random

pygame.init()
hgt = 50
wdt = 150
screen = pygame.display.set_mode((wdt*8,hgt*8),0,0)
clock = pygame.time.Clock()
FPS = 60
myfont = pygame.font.SysFont("calibri", 36)

grid = [[[(0),[(0),(0)],(0)] for y in range(hgt)] for x in range(wdt)] # color, pheremone (ant, strength), ant
playtime = 0.0
count=0
num_of_ants = 2
ants = [] # x, y, direction(0: right, 1: top, 2: left, 3: down)

background = pygame.Surface((screen.get_size())) # define background
background.fill((255,255,255)) # make it white by default

def drawGrid():
    for x in range(wdt):
        for y in range(hgt):
            if grid[x][y][0] == 0: pygame.draw.rect(background, (255,255,255), pygame.Rect((x*8,y*8), (8,8))) # draw white
            else: pygame.draw.rect(background, (0,0,0), pygame.Rect((x*8,y*8), (8,8))) # draw black
            if grid[x][y][2] != 0: pygame.draw.rect(background, (255,0,0), pygame.Rect((x*8,y*8), (8,8))) # draw ant
            if grid[x][y][1][0] != 0: # pher belongs to some ant
                if grid[x][y][1][1] == 5: pygame.draw.rect(background, (220,0,0), pygame.Rect((x*8,y*8), (8,8)))
                if grid[x][y][1][1] == 4: pygame.draw.rect(background, (200,0,0), pygame.Rect((x*8,y*8), (8,8)))
                if grid[x][y][1][1] == 3: pygame.draw.rect(background, (180,0,0), pygame.Rect((x*8,y*8), (8,8)))
                if grid[x][y][1][1] == 2: pygame.draw.rect(background, (160,0,0), pygame.Rect((x*8,y*8), (8,8)))
                if grid[x][y][1][1] == 1: pygame.draw.rect(background, (140,0,0), pygame.Rect((x*8,y*8), (8,8)))
def spawner():
    for n in range(num_of_ants):
        ants.append([random.randint(0,wdt-1), random.randint(0,hgt-1), random.randint(0,3)])
        grid[ants[n][0]][ants[n][1]][2] = 1
spawner()
def decay():
    for x in range(wdt):
        for y in range(hgt):
            if (grid[x][y][1][0] != 0 and grid[x][y][1][1] != 0): # if pher belongs to some ant
                grid[x][y][1][1] = grid[x][y][1][1] - 1
            if grid[x][y][1][1] == 0:
                grid[x][y][1][0] = 0 # delete pher
def flipColor(x):
    if grid[x[0]][x[1]][0] == 0: # if white
            grid[x[0]][x[1]][0] = 1 # make black
    else:
        grid[x[0]][x[1]][0] = 0 # else make white
def move(x):
    # move it in the respective direction
    if x[2] == 0: # right
        if x[0] == wdt - 1: x[0] = 0
        else: x[0] += 1
    if x[2] == 1: # top
        if x[1] == 0: x[1] = hgt - 1
        else: x[1] -= 1
    if x[2] == 2: # left
        if x[0] == 0: x[0] = wdt - 1
        else: x[0] -= 1
    if x[2] == 3: # down
        if x[1] == hgt - 1: x[1] = 0
        else: x[1] += 1
def forwardWalk(x):
    flipColor(x) # flip color
    grid[x[0]][x[1]][2] = 0 # ant is not present here now
    grid[x[0]][x[1]][1][0] = ants.index(x) + 1 # mark its pheremone
    grid[x[0]][x[1]][1][1] = 5 # leave its pheremone
    move(x) # move the ant
    grid[x[0]][x[1]][2] = 1 # ant is present here now  
def standardTurn(x):
    if grid[x[0]][x[1]][0] == 0: # if white
        x[2] = (x[2] - 1) % 4 # rotate clock-wise
    elif grid[x[0]][x[1]][0] == 1: # if black
        x[2] = (x[2] + 1) % 4 # rotate counter clock-wise
def pherCheck(x):
    pher = [0, 0]  # [mine (1 or 0), exists (1 or 0)]
    if grid[x[0]][x[1]][1][1] > 0:  # pher exists
        pher[1] = 1  # make exixt true
        if grid[x[0]][x[1]][1][0] == ants.index(x) + 1:  # is it mine tho
            pher[0] = 1  # its mine
        else:
            pher[0] = 0  # its not mine ew
    return pher
while 1:
    # make the bg of the count white
    count_bg = pygame.Surface((105,46))
    count_bg.fill((255,255,255))

    # enables quitting application
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # starts the timer which is used for controlling speed of ants
    milliseconds = clock.tick(FPS)
    playtime += milliseconds / 1000.0

    screen.lock()
    drawGrid()

    if playtime >= 0.01:
        decay()
        for ant in ants:
            isPher = pherCheck(ant)
            if isPher[1] == 1: # is there a pher under me
                if isPher[0] == 1: # its mine
                    if random.random() > 0.2: # i think its mine
                        forwardWalk(ant)
                    else: # wait i think its not mine
                        standardTurn(ant)
                        forwardWalk(ant)
                else: # its not mine
                    if random.random() > 0.8: # i think its mine
                        forwardWalk(ant)
                    else:
                        standardTurn(ant) # i think its not mine
                        forwardWalk(ant)
            else:
                standardTurn(ant) # normal, without pheremone headache
                forwardWalk(ant)
        playtime=0.0
        count+=1

    strings = str(count) # converts count into a string
    label = myfont.render(strings, 1, (0,0,0))

    screen.unlock()
    screen.blit(background, (0,0))
    screen.blit(count_bg, (0,0))
    screen.blit(label, (5, 5))
    pygame.display.update()