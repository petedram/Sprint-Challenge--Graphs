from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

'''



############

BFT but adding directions?

BFT_visit(graph, startVert):
    path = []
    visited = set()
    q = Queue()

    queue.enqueue(startVert)
    visited.add(startVert)

    while !q.isEmpty():
        u = q[0]  // Peek at head of queue, but do not dequeue!

        for v of u.get_neighbors():
            if v not in visited:
                q.enqueue(v)
                visited.add(v)
                #do something here to add path
        
        q.dequeue()
'''

# Load world
world = World()

#my custom graph
class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = {}

    def add_edge(self, v1, v2, destination):
        """
        Add a directed edge to the graph.
        """
        # if v2 not in self.vertices:
        #     # self.vertices[v2].add('unexplorered') #create it
        #     # self.vertices[v1].add(v2)
        #     pass
        # else:
        self.vertices[v1][v2] = destination

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]
    

def get_backtrack(direction_last_travelled):
    if direction_last_travelled == 'n':
        return 's'
    elif direction_last_travelled == 's':
        return 'n'
    elif direction_last_travelled == 'e':
        return 'w'
    elif direction_last_travelled == 'w':
        return 'e'

    



# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

##
##Find a way to add the best path so far to make it more efficient??

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)



def BFT_visit(graph, startVert):
    path = []
    visited = set()
    q = Queue()

    q.enqueue(startVert)
    visited.add(startVert)

    while q.size() > 0:
        u = q.queue[0]  # Peek at head of queue, but do not dequeue!
        
        possible = []
        for key, v in my_graph.get_neighbors(u).items():
            if v not in visited:
                possible.append((key,v))
        
        #pick one of the possibles
        if len(possible) > 0:
            next_node = random.choice(possible)
            q.enqueue(next_node[1]) #value = node id
            print('enqueuing neighbor: ', next_node[1])
            visited.add(u)
            path.append(next_node[0]) #key = direction to get to next node
            print('adding path: ', next_node[0])


        q.dequeue()
    
    return path

    #hitting dead-end and not backtracking...


def DFT_visit(v, prev_dir):
    last_room = player.current_room.id
    direction_last_travelled = v

    #Let's go!
    # print('travelling: ', v)
    player.travel(v)
    traversal_path.append(v)


    # print(f'Just arrived in room {player.current_room.id}, where the available exits are {player.current_room.get_exits()}')
    # print(f'Before arriving in this room, travelled from {last_room}')

    #go back and fill in the current room number, now that we know that   
    # print(f'last room {last_room} and direction {direction_last_travelled} and current room {player.current_room.id}')
    # my_graph.vertices[last_room][direction_last_travelled] == player.current_room.id
    my_graph.add_edge(last_room, direction_last_travelled,player.current_room.id )

    #build node + edges the first time we visit room
    if player.current_room.id not in my_graph.vertices:
        my_graph.add_vertex(player.current_room.id) #node
        for edge in player.current_room.get_exits(): #edges
            # print('adding edge', edge)
            my_graph.add_edge(player.current_room.id, edge, '?')
        # #add the edge from where we just came from
        # if my_graph.vertices[player.current_room.id][get_backtrack(v)] == '?':
        # print(f'adding backtrack edge? {player.current_room.id}, {get_backtrack(v)}, {last_room}')
        # my_graph.add_edge(player.current_room.id, get_backtrack(v), last_room)

        #start from here****************
        #   adding backtrack edge causes unknown issue.
        #   incomplete graph when not included...


    #latest status of graph
    # print('graph so far: ', my_graph.vertices)
    
    #ok where from here?
    # print(f'--move options', player.current_room.get_exits())
    possible_next = []
    for where_next in player.current_room.get_exits():
        if my_graph.vertices[player.current_room.id][where_next] == '?':
            possible_next.append(where_next)
    
    if len(possible_next) > 0:
        random.shuffle(possible_next)

        for item in possible_next:
            DFT_visit(item, item)
    
    # print('no more unexplored, recursing back')
    traversal_path.append(get_backtrack(prev_dir))
    player.travel(get_backtrack(prev_dir))


lowest_path = ['s', 'w', 'e', 'n', 'e', 'n', 's', 'w', 'w', 'w', 's', 'n', 'e', 'n', 'w', 'w', 'w', 's', 'n', 'e', 's', 'n', 'e', 'e', 's', 'e', 'n', 's', 'n', 's', 'w', 'n', 'w', 'w', 's', 'n', 'e', 'w', 'w', 's', 's', 'n', 's', 's', 's', 's', 's', 'n', 'n', 'w', 'w', 'e', 'e', 'n', 'n', 's', 'w', 'w', 'w', 'e', 'e', 'e', 'w', 'n', 's', 'n', 'w', 'e', 'w', 'w', 'e', 'w', 'w', 'e', 'w', 'e', 'e', 'e', 's', 'w', 'w', 's', 'n', 's', 'w', 'n', 's', 'e', 'w', 'n', 's', 'e', 'w', 'e', 'n', 'e', 'e', 'w', 'e', 'n', 's', 'e', 'w', 'e', 's', 'w', 's', 'n', 's', 'w', 'e', 'w', 'e', 'n', 'w', 'e', 's', 'n', 'e', 'w', 'e', 'n', 's', 's', 's', 's', 's', 'w', 's', 's', 'n', 'n', 'e', 'n', 'n', 'w', 'e', 'w', 's', 'w', 'e', 'n', 'w', 'w', 'w', 'e', 'e', 'e', 'w', 'w', 'n', 's', 'n', 's', 'w', 'w', 'e', 'n', 'w', 'w', 'n', 'w', 'e', 's', 'e', 'e', 's', 'n', 'w', 'n', 'n', 'w', 'n', 'e', 'n', 'w', 'e', 's', 'w', 'w', 'e', 's', 'e', 's', 's', 'n', 'n', 'w', 'n', 'w', 'e', 's', 'n', 'e', 'n', 'e', 'e', 'w', 'w', 'n', 's', 'n', 's', 'e', 'e', 'e', 'n', 'w', 'e', 's', 'w', 'e', 'n', 'e', 'n', 'n', 's', 'e', 'w', 's', 's', 'n', 'w', 'e', 's', 'n', 'w', 'e', 'n', 'w', 'w', 'w', 'w', 'e', 'n', 's', 'e', 'e', 'e', 'w', 'w', 'w', 'n', 'w', 'w', 'e', 'n', 'n', 's', 's', 'e', 'n', 's', 'n', 's', 'w', 'n', 'w', 'w', 'w', 'e', 'e', 'e', 'w', 'w', 'w', 'e', 'e', 'w', 'e', 'e', 'w', 'e', 'n', 's', 'w', 'e', 's', 'n', 's', 'e', 'w', 'w', 'w', 'e', 's', 'n', 's', 'n', 'w', 'e', 's', 'n', 'e', 'n', 's', 'e', 'w', 'e', 'n', 's', 's', 'e', 'w', 'w', 'e', 'e', 'w', 'n', 's', 'e', 'e', 'w', 'e', 'e', 'w', 'e', 'e', 'n', 's', 'e', 'n', 's', 'e', 'e', 'w', 'n', 's', 'w', 'w', 'e', 'e', 'n', 's', 'w', 'e', 'e', 'e', 'w', 'e', 'n', 'w', 'e', 'n', 'e', 'w', 'n', 's', 's', 's', 'e', 's', 'n', 'w', 'e', 's', 'e', 'e', 'e', 'w', 'w', 'n', 'n', 's', 'e', 'w', 's', 'w', 'e', 'n', 'e', 'n', 's', 'n', 'e', 'w', 'e', 'n', 'n', 'n', 's', 's', 's', 'n', 'e', 'n', 'n', 'e', 'w', 'n', 's', 's', 's', 'w', 'e', 'n', 'n', 'n', 's', 's', 'n', 'e', 'n', 'n', 's', 's', 'n', 'n', 'e', 'w', 'e', 'n', 's', 'e', 'w', 'e', 'e', 'e', 'w', 'w', 'n', 's', 'n', 's', 'e', 'n', 's', 'n', 's', 'e', 'w', 'w', 'e', 'n', 's', 'w', 'n', 's', 'w', 'n', 's', 'e', 'w', 'w', 's', 's', 'n', 's', 'w', 'n', 's', 's', 'n', 's', 's', 'n', 's', 'w', 'e', 'w', 'n', 'n', 'n', 's', 'n', 's', 's', 's', 'n', 's', 'e', 'w', 's', 'n', 's', 'w', 's', 'w', 's', 'n', 'n', 'n', 'n', 's', 'e', 'w', 's', 'n', 'e', 'n', 's', 'n', 'n', 's', 'n', 's', 's', 'w', 's', 'n', 'n', 'n', 's', 'n', 's', 's', 's', 'n', 'e', 'w', 's', 's', 'e', 'w', 's', 'n', 's', 'w', 'e', 'e', 's', 'n', 's', 's', 's', 'n', 'n', 'e', 's', 'n', 'w', 'e', 's', 's', 'e', 'w', 'n', 'e', 'e', 'w', 'w', 'e', 'e', 's', 'n', 'e', 'e', 'e', 'w', 'w', 'w', 'e', 'e', 'e', 'w', 'w', 'e', 'w', 'w', 'e', 'w', 's', 'e', 'w', 's', 's', 'e', 'n', 's', 'e', 'w', 'w', 's', 's', 'e', 'w', 'n', 'e', 'e', 'w', 'w', 'n', 'n', 'n', 's', 's', 's', 'e', 'e', 'w', 'w', 'e', 'w', 'n', 's', 's', 'e', 'e', 'w', 'e', 'w', 'w', 'n', 's', 'n', 'e', 'w', 'n', 's', 'n', 'n', 's', 'e', 'e', 'w', 'w', 'e', 'n', 's', 'w', 'e', 'e', 'w', 'w', 's', 'n', 'n', 's', 'n', 'n', 's', 'n', 'e', 'e', 's', 'n', 'e', 'w', 'w', 'e', 'e', 'w', 'w', 'e', 's', 'n', 'w', 'e', 'e', 'w', 'w', 'w', 's', 'n', 'n', 'e', 'w', 'w', 'w', 'e', 'w', 's', 'e', 'w', 'n', 's', 'n', 'e', 'w', 'n', 'w', 'e', 'w', 's', 's', 'n', 'n', 's', 'n', 'e', 'w', 'n', 'e', 'e', 'e', 'e', 'w', 's', 'e', 'e', 'e', 'e', 'w', 'w', 'w', 'w', 'n', 'w', 's', 'n', 'w', 'n', 'e', 'e', 'e', 'e', 'e', 'e', 's', 'n', 'w', 'w', 'w', 'w', 'w', 'n', 's', 'w', 's', 'n', 'e', 'n', 'e', 'n', 'e', 'e', 'e', 'e', 'w', 'w', 's', 'n', 'w', 's', 'n', 'w', 'n', 'e', 'n', 'n', 's', 's', 'e', 'n', 's', 'w', 'w', 's', 's', 'w', 'e', 'n', 'n', 'e', 'e', 'n', 'e', 'w', 'e', 'w', 's', 'w', 'e', 'w', 'w', 'e', 'n', 'n', 'e', 'e', 'e', 's', 'n', 'w', 'w', 'w', 'e', 'e', 'e', 's', 'n', 'w', 'e', 'w', 'w', 'e', 'w', 'w', 'e', 'w', 's', 's', 'n', 's', 'w', 'e', 'e', 'w', 'w', 's', 'n', 's', 's', 'n', 'e', 's', 'n', 'w', 'e', 'e', 's', 'e', 'e', 'w', 'w', 'e', 'e', 'e', 'w', 'e', 's', 'n', 's', 'n', 'w', 'w', 'w', 'e', 'w', 'n', 'w', 'e', 'e', 'n', 'e', 'w', 's', 'n', 'e', 'w', 's', 'n', 's', 'e', 'w', 'n', 's', 'w', 'e', 'w', 'w', 'e', 's', 'n', 'w', 's', 'n', 'w', 'e', 'w', 's', 'n', 'n', 's', 's', 'w', 'e', 'w', 's', 'w', 'e', 'e', 'e', 'e', 'e', 'e', 's', 'n', 'w', 'e', 'w', 'w', 'e', 'w', 'w', 'e', 'w', 'w', 'e', 'w', 'w', 'e', 'w', 'n', 's', 'w', 'e', 'w', 's', 'n', 's', 'e', 's', 'n', 'w', 'e', 'e', 's', 'e', 'e', 'e', 'n', 's', 'n', 's', 'e', 'w', 'n', 's', 'w', 'e', 'w', 'w', 'e', 'w', 'w', 'e', 'w', 'n', 's', 'n', 'w', 'e', 'e', 'e', 'w', 'e', 'w', 'w', 's', 'n', 'w', 'e', 'w', 'w', 'e', 's', 'n', 'w', 'n', 's', 'w', 's', 'n', 'w', 'e', 'w', 'w', 'e', 'n', 's', 'w', 'n', 'w', 'e', 'w', 'n', 'n', 'w', 'n', 'w', 'n', 's', 'e', 's', 'w', 'e', 'e', 'w', 'w', 'w', 'e', 'w', 'n', 'n', 'w', 'n', 's', 'e', 's', 's', 'w', 'w', 'n', 's', 'e', 'e', 'w', 'n', 's', 'n', 's', 'w', 'n', 'n', 's', 'w', 'e', 'w', 'n', 'n', 's', 'w', 'e', 's', 'w', 'e', 'w', 'w', 'e', 'w', 'e', 'e', 'n', 'w', 'w', 'w', 'e', 'e', 'n', 's', 'n', 'n', 's', 'n', 's', 's', 'w', 'n', 'n', 'n', 's', 's', 's', 'n', 'w', 'e', 'w', 'e', 'n', 'n', 's', 's', 'n', 's', 'w', 'e', 's', 'n', 's', 'w', 'w', 's', 'w', 'e', 'n', 'w', 'e', 'e', 'w', 'w', 'e', 'e', 'w', 's', 'w', 'e', 'n', 's', 'n', 'e', 'w', 'w', 'e', 'e', 'e', 'e', 'w', 'n', 's', 'e', 'n', 's', 'e', 's', 'n', 'n', 'n', 'n', 's', 's', 'n', 'n', 'w', 'e', 'n', 's', 'n', 'n', 's', 'n', 's', 's', 'w', 'e', 'n', 's', 's', 's', 'n', 's', 's', 'w', 'e', 's', 'n', 's', 'w', 'e', 'e', 'n', 'n', 'n', 'n', 's', 's', 's', 'n', 'n', 'n', 's', 's', 'n', 's', 's', 'n', 's', 's', 'w', 'e', 's', 'e', 'w', 'e', 'e', 'w', 'n', 's', 'e', 'n', 'n', 'w', 'n', 's', 'e', 'w', 'e', 's', 'n', 's', 's', 'n', 's', 'w', 'e', 'e', 'e', 'e', 'w', 'n', 'n', 'n', 'w', 'e', 's', 's', 'n', 'n', 'w', 'w', 'e', 'n', 's', 'n', 's', 'w', 'n', 'w', 'e', 's', 'n', 'w', 'e', 's', 'n', 's', 'e', 'n', 's', 'e', 's', 'n', 's', 's', 'n', 's', 'w', 'n', 's', 'e', 'w', 'e', 'n', 's', 's', 'n', 's', 'w', 'e', 'e', 'w', 'e', 'n', 's', 'w', 'e', 's', 'n', 'e', 'n', 's', 's', 'n', 's', 'n', 'n', 'n', 'w', 'e', 's', 'n', 'n', 'n', 's', 's', 'n', 'e', 'w', 'e', 'e', 'w', 'e', 'w', 'w', 'n', 'n', 's', 'e', 'e', 'n', 's', 'e', 'w', 'w', 'w', 'e', 'e', 'e', 'n', 's', 'e', 'w', 'e', 'w', 'n', 'e', 'w', 'n', 'w', 'n', 's', 'e', 'n', 'n', 'n', 's', 's', 's', 's', 'n', 'n', 'e', 'n', 'n', 's', 'e', 'w', 's', 'w', 'e', 'n', 'e', 'n', 'e', 'e', 'w', 's', 'n', 'w', 'n', 's', 's', 'n', 'n', 's', 's', 'n', 'e', 's', 'n', 'w', 'e', 'e', 'w', 'w', 'e', 's', 'n', 'w', 's', 'n', 'n', 's', 's', 'w', 's', 'n', 'n', 's', 's', 'n', 'e', 'w', 's', 'w', 'e', 'w', 'n', 'n', 's', 's', 'n', 's', 's', 'n', 'e', 'w', 's', 's', 'n', 'w', 'n', 'n', 's', 'n', 'n', 'w', 'e', 'n', 's', 's', 'n', 'n', 'e', 'w', 'e', 'e', 'w', 'e', 'w', 'w', 's', 's', 'n', 'w', 'w', 'e', 'n', 'w', 'e', 's', 'n', 'w', 'w', 'e', 'w', 'e', 'e', 's', 'n', 's', 'w', 's', 'n', 's', 's', 'n', 's', 's', 'w', 'w', 'w', 'e', 'e', 'n', 'w', 'e', 's', 'e', 'n', 's', 'e', 'n', 'n', 's', 's', 'w', 's', 'n', 's', 'e', 'w', 'e', 'w', 'n', 'e', 'n', 'n', 's', 's', 'n', 's', 'w', 'e', 'w', 's', 'n', 'w', 'n', 'n', 's', 'n', 's', 'w', 'n', 's', 'n', 's', 'e', 'n', 's', 's', 'n', 's', 'e', 'w', 'w', 'w', 'n', 's', 'w', 'w', 'e', 'e', 'w', 's', 'n', 's', 'w', 'e', 'w', 'e', 'n', 'w', 'w', 'n', 's', 'e', 'n', 's', 'n', 's', 'w', 'n', 's', 'e', 'w', 'e', 'n', 's', 'e', 'e', 'w', 's', 'n', 'e', 'n', 'n', 's', 'w', 'e', 'w', 'n', 's', 'n', 'n', 'w', 'e', 's', 'n', 'w', 'e', 's', 'n', 's', 's', 'e', 'n', 'n', 's', 'n', 'n', 's', 'n', 's', 's', 's', 'w', 'e', 's', 'w', 'e', 'e', 'e', 'w', 'e', 'n', 's', 'e', 'w', 'e', 'e', 'w', 's', 'n', 'n', 's', 'n', 'n', 'n', 'e', 'n', 's', 'e', 'n', 's', 's', 'n', 's', 's', 's', 'e', 'w', 'e', 'n', 's', 's', 'n', 's', 'e', 'n', 'e', 'e', 'w', 'n', 's', 'w', 's', 'e', 'w', 'e', 'w', 'n', 'e', 'n', 's', 'w', 'e', 'e', 'e', 'w', 'n', 's', 'n', 's', 'e', 'w', 'n', 's', 'w', 'n', 's', 'w', 'e', 'w', 's', 'n', 's', 'e', 'w', 'w', 'n', 's', 's', 'e', 'w', 'w', 'w', 'e', 'n', 's', 'w', 'e', 'e', 'w', 'w', 'w', 'e', 'w', 'n', 'e', 'w', 'n', 's', 's', 'e', 'w', 's', 's', 'n', 'e', 'w', 's', 'w', 'n', 's', 'n', 'n', 's', 'n', 'w', 'n', 'w', 'e', 'e', 'w', 's', 'e', 'w', 'n', 'e', 'w', 's', 'n', 'w', 'e', 'e', 'w', 's', 'n', 's', 'e', 'w', 'e', 's', 's', 'e', 'n', 's', 's', 'n', 's', 's', 's', 'n', 'w', 's', 'n', 'n', 's', 'w', 'e', 's', 's', 'n', 'w', 'e', 's', 'n', 'n', 's', 's', 'e', 'w', 'w', 'w', 'w', 'e', 'n', 's', 'w', 'w', 'e', 'n', 's', 'e', 'w', 'w', 'e', 'w', 'n', 's', 'e', 'w', 'w', 'w', 'e', 's', 'n', 'n', 'w', 'e', 'w', 'n', 's', 'w', 'e', 'w', 'e', 'n', 'w', 'e', 'w', 'e', 's', 'w', 'e', 'e', 's', 'e', 'w', 's', 'n', 'w', 'e', 's', 's', 'n', 'w', 'e', 'w', 'w', 'w', 'e', 'w', 'e', 'e', 's', 'n', 'e', 'w', 's', 'w', 'e', 'w', 'w', 'w', 'e', 'w', 'n', 's', 'w', 'w', 'e', 'n', 's', 'n', 's', 'w', 'e', 'n', 's', 'e', 'n', 's', 'e', 'w', 's', 'n', 's', 'w', 'e', 'w', 's', 'n', 'w', 'e', 's', 'e', 'w', 'e', 's', 'n', 's', 's', 'n', 's', 'w', 'n', 'w', 'e', 's', 'n', 's', 'e', 'w', 'e', 'e', 'w', 'n', 's', 'e', 's', 'n', 's', 'w', 'w', 's', 'w', 'e', 'n', 'e', 'w', 's', 'w', 's', 'n', 's', 'n', 'e', 'n', 's', 'n', 'e', 'w', 'e', 'e', 'n', 's', 'e', 'e', 'w', 'n', 's', 'e', 'e', 'w', 'e', 's', 'w', 'w', 'e', 's', 'w', 'e', 'n', 's', 'w', 's', 'n', 's', 'n', 'e', 'n', 's', 'n', 'w', 'w', 'w', 'e', 'e', 'w', 's', 'w', 'e', 's', 's', 's', 's', 's', 'e', 'w', 'n', 'e', 'w', 'n', 'n', 'n', 'n', 'n', 's', 's', 'w', 'w', 'e', 'e', 'w', 's', 's', 'n', 'n', 's', 'w', 'e', 'w', 'e', 's', 's', 's', 'n', 'n', 'w', 'e', 'w', 'e', 's', 'w', 'e', 'w', 'w', 'e', 'w', 'e', 'e', 's', 'n', 'n', 's', 'w', 'e', 'n', 'w', 'e', 'n', 'w', 'e', 'n', 's', 'n', 'w', 'w', 'e', 'w', 'w', 'e', 'w', 'e', 'e', 'e', 's', 'n', 'e', 'w', 'e', 's', 's', 's', 'e', 'w', 'n', 's', 's', 'e', 'w', 'n', 's', 'n', 'n', 's', 'e', 'w', 'n', 'n', 's', 'n', 'n', 's', 'n', 'n', 's', 'w', 'e', 'n', 'n', 's', 'w', 'w', 'e', 'w', 'e', 'e', 'n', 's', 's', 'n', 'n', 'w', 'e', 's', 'n', 'e', 'w', 'e', 'e', 's', 'n', 'e', 'n', 's', 'n', 'w', 'e', 'e', 's', 's', 's', 's', 's', 's', 'w', 'e', 'n', 'e', 's', 'n', 'w', 'n', 'n', 'n', 's', 's', 's', 'e', 'e', 'w', 'e', 's', 's', 'n', 'n', 's', 's', 's', 'n', 'e', 'w', 'e', 'w', 's', 'w', 'e', 'w', 'e', 'n', 'e', 'w', 'n', 'n', 's', 'n', 'w', 's', 'n', 'e', 'w', 'w', 'e', 'w', 'n', 's', 's', 'w', 'e', 'n', 's', 'n', 'n', 's', 'e', 'w', 'n', 'n', 's', 'n', 'n', 's', 'n', 'w', 's', 'w', 's', 's', 'n', 'w', 'e', 'n', 'e', 'w', 's', 'w', 'e', 'n', 's', 's', 'w', 'e', 'w', 'e', 'n', 'n', 's', 'w', 'e', 'n', 'e', 'w', 'e', 's', 's', 'n', 's', 'n', 'n', 'w', 'e', 'n', 's', 'n', 'e', 'w', 'e', 's', 'n', 'n', 's', 'n', 'n', 's', 'n', 'w', 'e', 'n', 'n', 's', 'n', 'n', 's', 'w', 'e', 'n', 'n', 's', 'w', 'e', 'n', 'n', 'n', 'e', 'w', 'e', 'e', 'w', 's', 'n', 'e', 'e', 'w', 'e', 's', 'n', 's', 'e', 'w', 'w', 's', 'w', 'e', 'w', 's', 's', 'n', 'n', 's', 's', 'n', 'n', 's', 'n', 'e', 'n', 'e', 'w', 'e', 'n', 's', 'e', 'w', 'e', 'n', 's', 'e', 'e', 'w', 's', 'n', 's', 's', 'w', 'w', 's', 'w', 'e', 'n', 'e', 'e', 'n', 'e', 'w', 'e', 's', 'n', 's', 'n', 'w', 's', 's', 's', 's', 'n', 'n', 'n', 's', 'e', 'e', 'w', 'w', 'e', 's', 'n', 's', 's', 'n', 's', 'n', 'n', 'e', 's', 'n', 's', 'e', 'n', 's', 'w', 's', 'e', 's', 'n', 'w', 'n', 's', 's', 'n', 's', 's', 's', 'e', 'w', 'n', 'n', 's', 's', 'e', 'w', 'n', 's', 'n', 'n', 's', 'n', 'n', 'e', 's', 's', 'e', 'e', 'w', 'w', 'n', 'e', 'w', 'e', 'w', 's', 'e', 'e', 'e', 'w', 'e', 'e', 'w', 'e', 'w', 'w', 'w', 'w', 'e', 'w', 'n', 's', 'n', 'e', 'w', 'n', 'w', 'e', 'w', 'n', 's', 's', 'n', 'n', 'e', 'n', 'e', 's', 's', 'n', 'n', 'w', 'e', 's', 's', 'n', 'n', 's', 'n', 'w', 'e', 'w', 's', 'w', 'e', 'w', 's', 'n', 'n', 'w', 'w', 'e', 's', 'n', 'w', 's', 's', 's', 'n', 's', 'e', 's', 's', 'n', 'n', 'w', 's', 'n', 's', 'n', 'e', 's', 's', 's', 's', 'n', 'e', 'w', 'n', 'w', 'e', 'w', 's', 's', 'n', 'n', 's', 's', 'n', 'n', 's', 'n', 'e', 's', 'e', 'e', 'e', 'n', 'e', 'w', 's', 'w', 'w', 's', 'e', 'e', 'w', 's', 's', 'n', 'n', 'w', 'n', 's', 's', 's', 'n', 'n', 's', 's', 'n', 'n', 's', 'n', 'e', 's', 's', 'n', 'n', 's', 'n', 'w', 'e', 'e', 's', 's', 'n', 'n', 's', 's', 'n', 'n', 's', 'n', 'w', 's', 'n', 'w', 'e', 'w', 'n', 's', 's', 'n', 'n', 'e', 'e', 'n', 'e', 'e', 's', 's', 'n', 'n', 'w', 's', 's', 'n', 'n', 's', 's', 'n', 'n', 's', 'n', 'e', 'e', 'w', 'e', 'w', 's', 's', 'e', 'w', 's', 'n', 's', 's', 'n', 's', 'n', 'n', 'e', 'w', 's', 'n', 'n', 'n', 's', 'n', 'e', 'w', 'w', 'e', 'w', 's', 'n', 'w', 's', 'n', 's', 'w', 'e', 'w', 'w', 'e', 'w', 's', 'n', 'w', 'n', 's', 's', 's', 's', 'n', 'n', 's', 'w', 'e', 'w', 's', 'n', 's', 'n', 'e', 's', 's', 'n', 's', 'n', 'n', 'n', 's', 'w', 'e', 'n', 'n', 'e', 'w', 'n', 's', 'n', 'w', 'e', 'n', 'n', 's', 'n', 'w', 'e', 'w', 's', 'n', 'n', 'n', 'n', 's', 'n', 'n', 's', 'e', 'w', 'n', 'w', 's', 's', 's', 's', 'n', 'n', 'n', 'n', 's', 's', 's', 's', 's', 'w', 'w', 's', 'e', 'w', 'n', 'e', 'n', 's', 'e', 's', 'n', 'n', 's', 's', 's', 's', 's', 's', 'n', 'n', 'n', 'n', 's', 's', 's', 's', 'n', 'n', 's', 'n', 'n', 's', 'n', 'n', 's', 'n', 'n', 'n', 's', 'w', 'n', 'n', 's', 'w', 'e', 'w', 'e', 'n', 'w', 'e', 'n', 'n', 's', 'w', 'w', 'e', 'e', 's', 'n', 'w', 'w', 's', 'n', 's', 'n', 'e', 'e', 'w', 'e', 's', 'n', 'n', 's', 'w', 'e', 's', 'n', 's', 'w', 'e', 'n', 's', 's', 'w', 'e', 's', 'e', 'w', 'w', 'w', 'n', 's', 'e', 'w', 'n', 's', 'e', 'w', 'e', 's', 'w', 'e', 's', 'n', 's', 'n', 'w', 's', 'n', 's', 'n', 'e', 's', 'n', 'e', 's', 's', 'n', 'n', 's', 's', 's', 'n', 's', 'n', 'n', 'n', 's', 'n', 'w', 'w', 'e', 'n', 's', 's', 'n', 'n', 'e', 'w', 'w', 'e', 'e', 'e', 'w', 'n', 's', 'e', 's', 'n', 'n', 's', 'n', 'n', 'n', 's', 'n', 'n', 's', 'n', 'n', 's', 'n', 'w', 'w', 'e', 'w', 'e', 's', 's', 'n', 'w', 'e', 's', 'n', 'n', 's', 'n', 'e', 'w', 'w', 'e', 'e', 's', 'n', 'e', 'w', 'e', 'n', 's', 's', 'n', 'n', 'e', 'w', 'n', 'e', 'w', 's', 'n', 'n', 'n', 's', 'e', 'w', 's', 'e', 'w', 's', 'n', 'w', 'e', 'w', 'n', 's', 'w', 'e', 's', 'w', 'e', 'n', 's', 'n', 'e', 'w', 'w', 'e', 'n', 's']

for item in range(0,10^10000):
    traversal_path = []
    move_history = []
    '''write code here'''

    my_graph = Graph()

    #First room
    #build node + edges
    my_graph.add_vertex(player.current_room.id) #node
    for edge in player.current_room.get_exits(): #edges
        # print('edge', edge)
        my_graph.add_edge(player.current_room.id, edge, '?')

    #DFT to complete the graph
    ##check if unexplorered path from current room, if y, pick random and go there.
    ###if no unexplored path from current room, go back to previous room ---> repeat this until back from where started.
    ###need to keep track of previous rooms?
    ####could have been to same room previous times... keep track of every step and backtrack in full?
    ####room_history.append upon entry. Where no unexplored, start an unexplorered count containing index position and -= from there until find unexplorered. Keep adding even when backtracking?

    # print(f'--move options', player.current_room.get_exits())
    first_potential = []
    for move_option in player.current_room.get_exits():
        # print(f'move option: {move_option} for room: {player.current_room.id}')
        if my_graph.vertices[player.current_room.id][move_option] == '?':
            first_potential.append(move_option)
        
    if len(first_potential) > 0:
        random.shuffle(first_potential)
        for item in first_potential:
            DFT_visit(item, item)

    print('recursion complete')
    # print('final graph: ', my_graph.vertices)
    # print('final path:', traversal_path)
    # print('path count: ', len(traversal_path))

    if len(traversal_path) < len(lowest_path):
        lowest_path = traversal_path

    print('lowest is: ', len(lowest_path))

# print(len(BFT_visit(my_graph, 0)))



# if move_option is None:
#     print('no move options, back tracking')
#     move_next = get_backtrack(direction_last_travelled)

# move_next = random.choice(move_next)
# print('next_move: ', move_next)

#store room_id of where came from before travelling
# last_room = player.current_room.id
# #update the direction last travelled
# direction_last_travelled = move_next
# #travel!
# player.travel(move_next)
######################################################



# player.travel(direction)

# for node in ancestors:
#     my_graph.add_vertex(node[0]) #Add parent nodes
#     my_graph.add_vertex(node[1]) #Add child nodes
#     #need to check if already exists? No dups.

# for node in ancestors:
#     my_graph.add_edge(node[1],node[0]) #create connections, ensure correct direction





# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
