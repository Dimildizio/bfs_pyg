from collections import deque
import heapq

class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))
        
    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0
    
class Node:
    def __init__(self, pos):
        self.pos = pos
        self.passable = True
        self.inside = []
        self.cost = 0

    def add(self, obj):
        self.inside.append(obj)
        if not obj.passable:
            self.passable = False
        
    def remove(self, obj):
        self.inside.remove(obj)
        if not obj.passable:
            self.passable = True

    def passable(self):
        return node.passable

class Field:
    def __init__(self, w,h):
        self.width = w
        self.height = h
        self.connections = ((1,0), (-1,0), (0,1), (0,-1),
                            (1,1), (-1,1),(1,-1),(-1,-1))
        self.cells = {}
        self.generate()

    def cell(self, pos):
        return self.cells[pos]

    def cost(self, from_node, to_node):
        fx,fy = from_node
        tx,ty = to_node
        inode = self.cell(to_node).cost
        return inode + 14 if (fx != tx and fy != ty) else inode + 10

    def generate(self):
        for x in range(self.width):
            for y in range(self.height):
                self.cells[(x,y)] = Node((x,y))

    def in_bounds(self, node):
        return 0 <= node[0] < self.width and 0 <= node[1] < self.height

    def show(self):
        for x in range(self.width):
            print()
            for y in range(self.height):
                if self.cells[(x,y)].inside:
                    print(self.cells[(x,y)].inside[0], end = ' ')
                else:
                    print('.', end = ' ')

    def plus_pos(self, o1,  o2):
        return (o1[0]+o2[0], o1[1] + o2[1])

    def find_neighbours(self, node):
        neighbours = [self.plus_pos(node, x) for x in self.connections]
        neighbours = filter(self.in_bounds, neighbours)
        neighbours = [x for x in neighbours if self.cells[x].passable]
        return neighbours

    def bfs(self, start, goal):
        frontier = deque()
        frontier.append(start)
        path = {start:None}
        
        while len(frontier) > 0:
            current = frontier.popleft()
            if current == goal:
                break
            for neighbour in self.find_neighbours(current):
                if neighbour not in path and self.cells[neighbour].passable:
                    frontier.append(neighbour)
                    path[neighbour] = current
        return path

    def heuristic(self, node1, node2):          #manhattan distance calc by x
        fx, fy = node1
        tx, ty = node2
        return 10 * (abs(fx - tx) + abs(fy - ty))
    
    def dijxtra(self, start, end):
        frontier = PriorityQueue()
        frontier.put((start), 0)
        path = {start:None}
        cost = {start:0}
        
        while not frontier.empty():
            current = frontier.get()

            if current == end:
                break
            for neigh in self.find_neighbours(current):
                next_cost = cost[current]+self.cost(current, neigh)
                if neigh not in cost or next_cost < cost[neigh]:
                    cost[neigh] = next_cost
                    priority = next_cost
                    frontier.put(neigh, priority)
                    path[neigh] = current
        for x in path:
            print(x,'cost:', cost[x])
        return path

    def astar(self, start, end):
        frontier = PriorityQueue()
        print('start', start)
        frontier.put(start, 0)
        path = {start:None}
        cost = {start:0}
        
        while not frontier.empty():
            current = frontier.get()

            if current == end:
                break
            for neigh in self.find_neighbours(current):
                next_cost = cost[current]+self.cost(current, neigh)
                if neigh not in cost or next_cost < cost[neigh]:
                    cost[neigh] = next_cost
                    priority = next_cost + self.heuristic(end, neigh)
                    frontier.put(neigh, priority)
                    path[neigh] = current
        for x in path:
            print(x,'cost:', cost[x])
        return path
    
    def reconstruct(self, start, goal):
        came = self.astar(start, goal)
        current = goal
        path = []
        #print(came)
        
        while current != start:
            print(current)
            path.append(current)
            current = came[current]
        #path.append(start)
        path.reverse()
        return path

class Object:
    def __init__(self, name, loc, pos, passable = False):
        self.loc = loc
        self.name = name
        self.passable = passable
        self.pos = self.port(pos)

    def __repr__(self):
        return self.name

    def port(self, pos):
        self.loc.cells[pos].add(self)
        return pos

    def move(self, position):
        self.loc.cells[self.pos].remove(self)
        self.loc.cells[position].add(self)
        self.pos = position

    def goto(self, position):
        a = self.loc.reconstruct(self.pos, position)
        for x in a:
            z = self.pos
            print('position',z)
            self.move(x)
            Object('-', self.loc, z, passable = True)


a = Field(10,10)
m = Object('W', a, (0,0))
l = [2,4]
for y in l:
    for x in range(8):
        Object('I', a, (x, y))
Object('I', a, (7,3))
a.cells[0,2].passable = True
a.cells[0,2].inside = []
for x in range(10):
    for y in range(10):
        a.cells[y,x].cost = x

a.show()
m.goto((0,9))
a.show()

        
