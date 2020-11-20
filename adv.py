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
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

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


def DFT_visit(v):
    last_room = player.current_room.id
    direction_last_travelled = v

    #Let's go!
    print('travelling: ', v)
    player.travel(v)

    print(f'Just arrived in room {player.current_room.id}, where the available exits are {player.current_room.get_exits()}')
    print(f'Before arriving in this room, travelled from {last_room}')

    #go back and fill in the current room number, now that we know that   
    print(f'last room {last_room} and direction {direction_last_travelled} and current room {player.current_room.id}')
    # my_graph.vertices[last_room][direction_last_travelled] == player.current_room.id
    my_graph.add_edge(last_room, direction_last_travelled,player.current_room.id )

    #build node + edges the first time we visit room
    if player.current_room.id not in my_graph.vertices:
        my_graph.add_vertex(player.current_room.id) #node
        for edge in player.current_room.get_exits(): #edges
            print('adding edge', edge)
            my_graph.add_edge(player.current_room.id, edge, '?')
        # #add the edge from where we just came from
        # if my_graph.vertices[player.current_room.id][get_backtrack(v)] == '?':
        print(f'adding backtrack edge? {player.current_room.id}, {get_backtrack(v)}, {last_room}')
        # my_graph.add_edge(player.current_room.id, get_backtrack(v), last_room)

    #latest status of graph
    print('graph so far: ', my_graph.vertices)
    
    #ok where from here?
    print(f'--move options', player.current_room.get_exits())
    for where_next in player.current_room.get_exits():
        if my_graph.vertices[player.current_room.id][where_next] == '?':
            DFT_visit(where_next)
        else:
            print('no more unexplored, recursing back')



traversal_path = []
move_history = []
'''write code here'''

my_graph = Graph()

#First room
#build node + edges
my_graph.add_vertex(player.current_room.id) #node
for edge in player.current_room.get_exits(): #edges
    print('edge', edge)
    my_graph.add_edge(player.current_room.id, edge, '?')

#DFT to complete the graph
##check if unexplorered path from current room, if y, pick random and go there.
###if no unexplored path from current room, go back to previous room ---> repeat this until back from where started.
###need to keep track of previous rooms?
####could have been to same room previous times... keep track of every step and backtrack in full?
####room_history.append upon entry. Where no unexplored, start an unexplorered count containing index position and -= from there until find unexplorered. Keep adding even when backtracking?

print(f'--move options', player.current_room.get_exits())
for move_option in player.current_room.get_exits(): #thinks w is move option from 2??
    print(f'move option: {move_option} for room: {player.current_room.id}')
    if my_graph.vertices[player.current_room.id][move_option] == '?':
        DFT_visit(move_option)


print('recursion complete')
print('final graph: ', my_graph.vertices)



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
