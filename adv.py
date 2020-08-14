from room import Room
from player import Player
from world import World

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
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

'''
Notes:

Example room graph:
room_graph = {
    0: [(3, 5), {'n': 1}],
    1: [(3, 6), {'s': 0, 'n': 2}],
    2: [(3, 7), {'s': 1}]
}

# reference to the first room
room_graph[room_id] = list[Tuple (3, 5), dict w/ possible exits {'n': 1}]
room_graph[0] = [(3, 5), {'n': 1}] # reference to the first room
room_graph[0][0] = (3, 5) # x,y coords?
room_graph[0][1] = {'n': 1} # list of possible exits

Useful commands:
# Returns the current room's id ('int')
    - player.current_room.id
    # 0
# Returns the current room's exits ('list')
    - player.current_room.get_exits()
    # ['n', 's', 'w', 'e']
# Moves the player in the direction passed (direction = 'str')
    - player.travel(direction)
'''


# Returns the opposite direction (i.e. 'n' -> 's')
def get_opposite_direction(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'w':
        return 'e'
    elif direction == 'e':
        return 'w'


# Generates a traversal path to explore all rooms
def generate_traversal_path(graph):
    # Container for generated path
    generated_path = []
    # Container used for backtracking
    backtrack = []
    # Used to keep track of which rooms have been visited
    visited = {}
    # Used to keep track of which rooms have unexplored paths
    unexplored = {}

    # Run while there are unexplored rooms
    while len(visited) < len(room_graph):
        # Add the starting point to visited and unexplored
        if len(visited) == 0:
            current_room = player.current_room.id
            current_exits = player.current_room.get_exits()
            # room: {0: ['n', 's', 'w', 'e']}
            visited[current_room] = current_exits
            # unexplored: {0: ['n', 's', 'w', 'e']}
            unexplored[current_room] = current_exits

        # Check to see if the current room has been visited
        if player.current_room.id not in visited:
            # Add the current room to unexplored and visited
            visited[player.current_room.id] = player.current_room.get_exits()
            unexplored[player.current_room.id] = player.current_room.get_exits()

        # If there's no more directions to go in the current room, then backtrack
        while len(unexplored[player.current_room.id]) < 1:
            opposite_direction = backtrack.pop()
            generated_path.append(opposite_direction)
            player.travel(opposite_direction)

        # Grab a direction to move in
        move = unexplored[player.current_room.id].pop()
        # Add it to the path
        generated_path.append(move)
        # Add the opposite of the move to the backtrack list
        # (this is used to help backtrack when there aren't any new rooms to check in the current room)
        backtrack.append(get_opposite_direction(move))
        # Moves the player to the room to update the current room
        player.travel(move)

    # Returns a list of directions
    return generated_path


# Update traversal_path
traversal_path.extend(generate_traversal_path(room_graph))

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
