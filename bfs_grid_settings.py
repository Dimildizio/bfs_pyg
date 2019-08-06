
FPS = 60
TILE = 32
BORDER_W, BORDER_H = 20, 15
WIDTH, HEIGHT = TILE*BORDER_W, TILE*BORDER_H

#colours
BLACK = (0,0,0)
WHITE = (255,255,255)
DARKGRAY = (50,50,50)
LIGHTGRAY = (150,150,150)
GREEN = (50,200,50)
RED = (220,30,30)
YELLOW = (255,255,0)
BLUE = (50, 180,180)

GET_TILE = lambda pos: (pos[0] // TILE * TILE, pos[1] // TILE * TILE)
GET_NODE = lambda pos: (pos[0]//TILE, pos[1]//TILE)
GET_PX = lambda pos: (pos[0]*TILE, pos[1]*TILE)
IN_BORDER = lambda pos: 0 <= pos[0] < BORDER_W and 0 <= pos[1] < BORDER_H