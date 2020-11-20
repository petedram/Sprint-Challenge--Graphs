from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

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
traversal_path = []
'''write code here'''

my_graph = Graph()

#build node + edges for the first room
my_graph.add_vertex(player.current_room.id) #node
for edge in player.current_room.get_exits():
    print('edge', edge)
    my_graph.add_edge(player.current_room.id, edge, '?')

##Next Step: add key:value pairs in edge set i.e. 'n':'?'


print('current room: ', player.current_room.id)
print('exits: ', player.current_room.get_exits())
print('graph so far: ', my_graph.vertices)

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
