from room import Room
from player import Player
from world import World
from stack import Stack

import random
from ast import literal_eval

# Load world
world = World()


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

# Function for returning from dead end
def backtrack(dir):
    if dir == "s":
        return "n"
    elif dir == "n":
        return "s"
    elif dir == "w":
        return "e"
    elif dir == "e":
        return "w"

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

moves = Stack()

# While rooms visited is less than total rooms
while len(visited_rooms) < len(world.rooms):
    # Get exits
    exits = player.current_room.get_exits()
    # Possible directional moves
    directions = []

    # Add current room to visited rooms
    visited_rooms.add(player.current_room)

    for exit in exits:
        # If the exit exists and the room hasn't been visited, plan a move in that direction
        if (exit is not None) and (player.current_room.get_room_in_direction(exit) not in visited_rooms):
            directions.append(exit)

    # If moves are available
    if len(directions) > 0:
        # Random direction picker
        random_dir_i = random.randint(0, len(directions)-1)
        # Add direction to moves
        moves.push(directions[random_dir_i])
        # Move in that direction
        player.travel(directions[random_dir_i])
        # Add move to traversal path
        traversal_path.append(directions[random_dir_i])

    # If no moves available
    else:
        # Last move
        last = moves.pop()
        # Backtrack to last move
        player.travel(backtrack(last))
        # Add backtrack to traversal path
        traversal_path.append(backtrack(last))


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
