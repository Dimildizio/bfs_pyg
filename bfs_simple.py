'''implementation of bfs with simple visualization
border = num    -  square grid limit
matrix     - Node() in a YxX grid dictionary 
my_position = YxX   - start position
path     - result of bfs
'''

from random import randint


class Node():
	def __init__(self):
		self.occupied = False if randint(0,3) else True				#1 in 4 tiles is occupied

def neighbours(cell, goal):
	#find neighbours of the cell
	#args: cell - intital cell to find neighbours from, goal - destination of pathfinding to add to list if goal occupied
	#diagonals prioritized (first in output) so looks weird
	lmt, brd = lambda l: (l-1, l+2), lambda b: 0 <= b < border
	dest = lambda c: brd(c[0]) and brd(c[1]) and (c == goal or not matrix[c].occupied) and c != cell
	return [(y,x) for y in range(*lmt(cell[0])) for x in range(*lmt(cell[1])) if dest((y,x))]


def bfs(start, goal):
	#find the path from goal to start. reverse.
	#args: start: initial point to start pathfinding from. goal: destination point
	frontier = [start]
	_path = {start:False}
	while len(frontier) > 0:
		current = frontier.pop(0)
		if current == goal: 
			print('goal reached')
			break
		for n in neighbours(current, goal):
			if n not in _path:
				frontier.append(n)
				_path[n] = current
	if current != goal: 
		show()
		return (str(goal)+" can't be reached")
	step, way = goal, []
	while step != start:
		way.append(step)
		step = _path[step]
	way.reverse()
	return way

def show():
	#prints the matrix
	for y in range(border):
		for x in range(border):
			if (y,x) == my_position:
				print('@', end = ' ')
			elif (y,x) in path:
				print('0', end = ' ')
			else:
				print('!' if matrix[(y,x)].occupied else '.', end = ' ')
		print()

if __name__ == '__main__':

	border = 20															#numXnum matrix
	matrix = {(y, x):Node() for y in range(border) for x in range (border)}
	my_position = 2, 3
	path = bfs(my_position, (19,19))
	show()
