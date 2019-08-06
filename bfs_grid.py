'''This and example of Breadth first pathfinding algorithm
all settings to play with in file bfs_grid_settings
everything is scallable with the TILE variable in bfs_grid_settings'''

import pygame as pg
import sys
from bfs_grid_settings import *


class Game:
	def __init__(self):
		#setting up pygame and running
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.timer = pg.time.Clock()
		self.running = True
		self.grid = MyGrid()
		self.grid_flag = False
		self.mainloop()

	def handle_events(self):
		#handles input in pygame widnow
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.running = False
				pg.quit()
				sys.exit()
			if event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 3:
					self.grid.add_wall()
				elif event.button == 2:
					self.grid.change_start()
				elif event.button == 1:
					self.grid.change_goal()
			elif event.type ==pg.KEYDOWN:
				if event.key == pg.K_SPACE:
					self.grid.no_walls()
				elif event.key == pg.K_g:
					self.grid_flag = False if self.grid_flag else True
			elif pg.mouse.get_pressed()[2]:
				self.grid.add_wall(True)

	def mainloop(self):
		#main loop of the game
		while self.running:
			self.timer.tick(FPS)
			self.handle_events()
			self.draw()

	def draw_grid(self):
		#makes a grid if grid flag is True 
		for x in range(0, WIDTH, TILE):
			pg.draw.line(self.screen, LIGHTGRAY, (x,0), (x, HEIGHT))
		for y in range(0, HEIGHT, TILE):
			pg.draw.line(self.screen, LIGHTGRAY, (0, y), (WIDTH, y))


	def draw(self):
		#Main draw method. draws everything
		self.screen.fill(DARKGRAY)
		if self.grid_flag:
			self.draw_grid()
		self.grid.draw_rects(self.screen)
		pg.display.flip()


class MyGrid:
	def __init__(self):
		self.walls = set()
		self.start = TILE,TILE
		self.goal = False

	def add_wall(self, pressed = False):
		#on mouse click places the wall onto empty position, if the position is occupied by wall - removes wall.
		#arg: pressed - draws walls if the button is held
		wall = GET_TILE(pg.mouse.get_pos())
		if wall != self.start:
			if pressed:
				self.walls.add(wall)
			else: 
				self.walls.remove(wall) if wall in self.walls else self.walls.add(wall)

	def no_walls(self):
		#delete all walls
		self.walls = set()

	def change_start(self):
		#change the position from wich the pathfinding is counted
		pos = GET_TILE(pg.mouse.get_pos())
		if pos in self.walls:
			self.walls.remove(pos)
		self.start = pos

	def change_goal(self):
		#changes the pathfinding destination point
		goal = GET_TILE(pg.mouse.get_pos())
		self.goal = goal if goal != self.start and goal not in self.walls else False

	def draw_rect(self, pos, colour, screen):
		#draws a TILE size rectangle. 
		#args - pos - pixel position, colour - RGB colour, screen - surface to draw on
		x,y = pos
		rect = pg.Rect(x+1, y+1, TILE-1, TILE-1)
		pg.draw.rect(screen, colour, rect)

	def draw_rects(self, screen):
		#draws walls and pathfinding path. 
		#arg: surface to draw on
		self.draw_path(screen)
		for wall in self.walls:
			self.draw_rect(wall, WHITE, screen)
		self.draw_rect(self.start, GREEN, screen)

	def draw_path(self, screen):
		#calls bfs and draws the result. 
		#arg: surface to draw on
		if self.goal:
			path = self.bfs()
			if path:
				for tile in path:
					self.draw_rect(GET_PX(tile), RED, screen)
				self.draw_rect(self.goal, YELLOW, screen)

	def bfs(self):
		#pathfinding algorithm. finds neighbours of the cell starting from the 'start' and ending at 'goal' if possible
		start, goal = GET_NODE(self.start), GET_NODE(self.goal)
		frontier = [start]
		path = {start:False}
		while len(frontier) > 0:
			current = frontier.pop(0)
			if current == goal: 
				break
			for n in self.neighbours(current):
				if n not in path:
					frontier.append(n)
					path[n] = current
		if current != goal: 
			self.goal = False
			return 
		step, way = goal, []
		while step != start:
			way.append(step)
			step = path[step]
		way.reverse()
		return way

	def neighbours(self, cell):
		#return surrounding cells of the cell if the exist and not occupied
		#args: cell - cell to find neighbours
		cx,cy = cell
		lmt = lambda l: range(l-1, l+2)
		dest = lambda pos: (IN_BORDER(pos) and (GET_PX(pos) not in self.walls) and pos != cell)
		ilist = [(x, y) for x in lmt(cx) for y in lmt(cy) if dest((x, y))]
		#since its bfs and not dijkstra we dont have weights (diag=vert*2**0.5)) and diagonals come first in list
		#to prioritize vertcals and horizontals over diagonals we need to rearrange the list
		for pos in range(len(ilist)):
			x,y = ilist[pos]
			if x == cx or y == cy: 
				ilist.insert(0, ilist.pop(pos))
		return ilist

if __name__ == '__main__':
	pg.init()
	g = Game()


		