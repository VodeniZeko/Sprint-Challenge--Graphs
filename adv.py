from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# The collection Module in Python provides different types of containers. A Container is an object that is used to store different objects and provide a way to access the contained objects and iterate over them.
# https://docs.python.org/3/library/collections.html#collections.deque

from collections import deque

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
# print(world.print_rooms())
# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)
# TODO
# print(player.current_room)


# Fill this out with directions

# Player path
traversal_path = []

# backwards player path
steps_for_back = []
visited = {}

# for backin up
backwards_directions = {"n": "s", "e": "w", "w": "e", "s": "n"}


def starting_point():
    exits = player.current_room.get_exits()
    # TODO
    # print("exists avilable", exits)
    visited[player.current_room.id] = deque()
    # TODO
    # print("here", visited[player.current_room.id])
    for each_exit in exits:
        visited[player.current_room.id].append(each_exit)
        # TODO
        # print("here", visited[player.current_room.id])


def go_forward():
    # get first direction
    direction = visited[player.current_room.id].pop()
    # TODO
    # print("directions here", direction)
    # go there
    player.travel(direction)

    # so we know where we have been add the direction in step_back array
    steps_for_back.append(backwards_directions[direction])
    # print(steps_for_back)
    # print("directions aagain", direction)

    if player.current_room.id not in visited:
        # Add current room to visited
        starting_point()
        # also remove steps at id cus we already been there (main_maze.txt)
        visited[player.current_room.id].remove(backwards_directions[direction])

    # Add the direction we traveled to traversal_path
    traversal_path.append(direction)
    # TODO
    # print(traversal_path)


def go_back():
    # Go back one room and check again
    direction = steps_for_back.pop()
    traversal_path.append(direction)
    player.travel(direction)


starting_point()
# TODO
# go_forward()
while len(visited) < 500:
    if len(visited[player.current_room.id]) > 0:
        go_forward()
        # print("going forwards")
    else:
        go_back()
        # print("going_back")

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

# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
