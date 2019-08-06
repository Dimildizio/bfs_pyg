import sprites
import queue
import heapq
from collections import deque
from constants import *


TURN = 0

class PriorityQueue:
    def __init__(self):
        self.tiles = []

    def put(self, node, cost):
        heapq.heappush(self.tiles, (cost, node))
        
    def get(self):
        return heapq.heappop(self.tiles)[1]

    def empty(self):
        return len(self.tiles) == 0


class Node:
    def __init__(self, pos, cell_effects = False):
        self.pos = pos
        self.inside = []
        self.occupied = False
        self.neighbours = []
        self.cell_effects = cell_effects if cell_effects else []
        self.sprite = 'g.png'
        self.visited = False
        self.cost = 0

    def __repr__(self):
        return str(self.pos)+': '+str(self.inside)

    def check_occupied(self):
        for x in self.inside:
            if not x.passable:
                self.occupied = True
                return True
        self.occupied = False

    def add_to_cell(self, obj):
        self.inside.append(obj)
        self.check_occupied()
        self.terra_effect(obj)

    def remove_from_cell(self, obj):
        if obj in self.inside:
            self.inside.remove(obj)
            #print('inside:', self.inside)
        self.check_occupied()
                   
    def terra_effect(self, obj = False, timer = False):
        if self.cell_effects:
            obj = [obj] if obj else [x for x in self.inside if x in Locations.current.all_creatures] 
            if obj:
                for x in obj:
                    for effect in self.cell_effects:
                        effect.happen(x, timer = timer)

class Field:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.cells = {}
        self.create_nodes()
        self.order = []
        self.order_len = False
        self.order_moved = False
        self.contains = {'structures': set(), 
                         'objects' : set(), 
                         'creatures' : set(),
                         'playable' : set(),
                         'terrain_effects':set()}

    @property
    def all_creatures(self):
        return self.contains['creatures'] | self.contains['playable']

    def __repr__(self):
        return str(self.cells)

    def bounds(self, cell):
        x,y = cell
        mx,my = self.maxsize
        return 0 <= x < mx and 0 <= y < my

    def collision(self, pos):           #check  boundaries and cell occupied
        return (not self.cells[pos].occupied and self.bounds(pos))

    def cost(self, from_node, to_node):
        fx,fy = from_node
        tx,ty = to_node
        inode = self.cells[to_node].cost
        return inode + DIAGONAL_COST if (fx != tx and fy != ty) else inode + VH_COST

    def create_nodes(self):
        mx, my = self.maxsize
        for x in range(mx):
            for y in range(my):
                self.cells[x, y] = Node((x,y))             
                #creating neighbours
                directions = [(x+1,y), (x, y+1), (x-1,y), (x,y-1), (x-1,y-1),
                              (x-1,y+1), (x+1,y+1), (x+1, y-1)]
                for n in directions:
                    if self.bounds(n):
                        self.cells[x, y].neighbours.append(n)

    def add_in(self, pos, obj):            
        cell = self.cells[pos]
        cell.add_to_cell(obj)
        return pos

    def remove(self, obj):
        cell = self.cells[obj.pos]
        cell.remove_from_cell(obj)

    def reposition(self, obj, pos):
        if self.bounds(pos):
            self.remove(obj)
            self.add_in(pos, obj)
            return True
    
    def port_object(self, pos, obj):
        #print('position :',pos)
        if self.bounds(pos) and (obj.passable or not self.cells[pos].occupied):
            self.add_in(pos, obj)
            #print(self.cells[pos].inside, self.cells[pos].occupied, end = ' ')
        else:
            print('NO pos: ', pos)
            pos = self.port_object(choice(self.cells[pos].neighbours), obj)
        return pos




                                    #PATHFINDING


    def heuristic(self, node1, node2):          #manhattan distance calc by x
        fx, fy = node1
        tx, ty = node2
        return HEURISTIC_DIST_MULT * (abs(fx - tx) + abs(fy - ty))

    def find_neighbours(self, node, goal, unpassable = True):
        nx,ny = node
        neighbours = [(nx+x[0], ny+x[1]) for x in NODE_DIRECTIONS]
        neighbours = filter(self.bounds, neighbours)
        if unpassable:
            neighbours = [x for x in neighbours if not self.cells[x].occupied or x == goal]
        else: neighbours = list(neighbours)
        return neighbours

    def astar(self, start, goal):
        my_q = PriorityQueue()
        my_q.put(start, 0)
        path, cost = {start:None}, {start:0}

        while not my_q.empty():
            current = my_q.get()
            if current == goal:
                break
            for n in self.find_neighbours(current, goal):
                next_cost = cost[current] + self.cost(current, n)
                if n not in cost or next_cost < cost[n]:
                    cost[n] = next_cost 
                    priority = next_cost + self.heuristic(goal, n)   #without heuristic makes dijkstra algorithm
                    my_q.put(n, priority)
                    path[n] = current
        return path

    def bfs(self, start, goal):
        frontier = deque()
        frontier.append(start)
        path = {start:None}
        
        while len(frontier) > 0:
            current = frontier.popleft()
            if current == goal:
                break
            for neighbour in self.find_neighbours(current, goal, unpassable = False):
                if neighbour not in path:
                    frontier.append(neighbour)
                    path[neighbour] = current
        return path


    def path_algorithm(self, start, goal, bfs = False):

        came = self.bfs(start, goal) if bfs else self.astar(start, goal)    
        current = goal
        path = []
        while current != start:
            #print(came[current])
            path.append(current)
            current = came[current]
        path.reverse()
        return path


    def initiative_order(self):
        for x in self.all_creatures:
            if x.consciousness.val_zero():
                initiative = x.roll_initiative()
                insertion = False
                if self.order:
                    for obj in self.order:
                        if x.initiative > obj.initiative:
                            insertion = self.order.index(obj)
                    if insertion:
                        self.order.insert(insertion, x)
                    else: self.order.append(x)
                else: self.order.append(x)
        self.order.reverse()
        self.order_len = len(self.order)
        #for x in self.order:
            #print(x.name, 'initiative: ', x.initiative)


    def make_turn(self):

        if self.contains['playable']:
            Locations.game.player = False
            if self.order:
                actor = self.order.pop()
                Locations.actor = actor
                actor.target = False if actor.target not in self.all_creatures else actor.target
                actor.moved = False
                self.cells[actor.pos].terra_effect(actor, timer = True)
                if not actor.hp.val_zero():
                    return self.make_turn()
                print(f'\n\nTurn for #{self.order_len - len(self.order)}:', actor.name, 'player: ', actor.is_player)
                Locations.game.act_log_add('')
                Locations.game.act_log_add(f'Turn for {actor.name}')
                if actor.is_player:
                    Locations.game.player = actor
                else: self.make_turn()
                #elif actor.select_target():
                    #actor.ai_act()
                #actor.game.ud()
            else: 
                self.next_turn()
        else: Locations.game.set_game_mode('end')


    def countdown_cell_effects(self):
        effects = self.contains['terrain_effects'].copy()
        for effect in effects:
            effect.new_turn()

    def next_turn(self):
        for actor in self.all_creatures:
            actor.bodycheck()
        global TURN
        TURN += 1
        self.countdown_cell_effects()
        print('Turn: ', TURN)
        self.order = []
        self.initiative_order()
        self.make_turn()



class Locations:
    current = False
    game = False
    actor = False
    all_locs = []

    @classmethod
    def generate(cls, x, y):
        location = Field((int(x), int(y)))
        cls.current = location
        cls.all_locs.append(location)
        return cls.current

    @classmethod
    def ud(cls):
        if cls.game.mode == 'game':
            cls.game.get_los()
            #cls.game.ud() #gets obsolete with frame screen update


if __name__ == '__main__':

    current_location = Locations.generate(15, 15)

