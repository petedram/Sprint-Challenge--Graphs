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
traversal_path = []

#Depth
stack=[] #simple array stack
stack.append(world.starting_room)
visited = set()
while stack:
    current_room = stack.pop()
    if current_room not in visited:
        visited.add(current_room)
    if current_room.w_to and current_room.w_to not in visited:
        traversal_path.append("w")
        stack.append(current_room.w_to)
    elif current_room.s_to and current_room.s_to not in visited:
        traversal_path.append("s")
        stack.append(current_room.s_to)
    elif current_room.n_to and current_room.n_to not in visited:
        traversal_path.append("n")
        stack.append(current_room.n_to)
    elif current_room.e_to and current_room.e_to not in visited:
        traversal_path.append("e")
        stack.append(current_room.e_to)
    elif len(visited) == len(room_graph):
        break
    else:

        #Breadth
        simple_queue = [] #simple array queue
        simple_queue.append(current_room)
        paths = [[]]
        while simple_queue:
            visited_room = simple_queue.pop(0)
            path = paths.pop(0)
            if (visited_room.n_to and visited_room.n_to not in visited) or (visited_room.s_to and visited_room.s_to not in visited) or (visited_room.w_to and visited_room.w_to not in visited) or (visited_room.e_to and visited_room.e_to not in visited):
                simple_queue.clear()
                traversal_path.extend(path)
                stack.append(visited_room)
            else:
                if visited_room.n_to:
                    new_path = path.copy()
                    new_path.append("n")
                    paths.append(new_path)
                    simple_queue.append(visited_room.n_to)
                if visited_room.s_to:
                    new_path = path.copy()
                    new_path.append("s")
                    paths.append(new_path)
                    simple_queue.append(visited_room.s_to)
                if visited_room.w_to:
                    new_path = path.copy()
                    new_path.append("w")
                    paths.append(new_path)
                    simple_queue.append(visited_room.w_to)
                if visited_room.e_to:
                    new_path = path.copy()
                    new_path.append("e")
                    paths.append(new_path)
                    simple_queue.append(visited_room.e_to)


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
