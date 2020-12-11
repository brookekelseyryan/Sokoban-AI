import sokoban as sb
import numpy as np
import queue as q
import board as b
import random
import pprint
np.set_printoptions(edgeitems=30, linewidth=100000,formatter=dict(float=lambda x: "%.3g" % x))


# String constants for each component of the Sokoban puzzle
WALL = "#"
AGENT = "@"
GOAL = "."
BOX = "$"

# Moves
UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"

#
# getReachableBoxes()
# parameters: board, agent
# returns: dictionary of boxes
#
def getReachableBoxes(board, agent):

    frontier = q.Queue()                                            #create frontier queue
    start = agent.coordinates
    frontier.put((start, []))                                       #put agent's current location onto frontier (node, [path])
    visited = {agent.coordinates}                                   #create set of reached spaces, add agent's current location
    boxes = {}                                                      #dictionary of boxes key=coordinates: value=[moves]

    while not frontier.empty():                                     #while the frontier is not empty
        node, path = frontier.get()                                 #pop from frontier
        neighbors, boxes = expand(board, node, boxes, path)         #expand the node, get its neighbor children and boxes
        for neighbor in neighbors:                                  #for each neighbor
            if neighbor not in visited:                             #if neighbor has not been visited
                visited.add(neighbor)                               #add neighbor to visited
                frontier.put((neighbor, path + [neighbor]))         #put neighbor onto frontier as well as path to neighbor

    return boxes

#
# expand()
# parameters: board, node, boxes, path
# returns: list of neighbors, dictionary of boxes
#
def expand(board, node, boxes, path):
    neighbors = []

    ##UP##
    if board[node[0] - 1][node[1]] != WALL:                         #if UP is not a wall
        if board[node[0] - 1][node[1]] == BOX:                          #if UP is a box
            if board[node[0] - 2][node[1]] != WALL:                         #if you can push the box UP
                if (node[0] - 1, node[1]) in boxes:                             #if box exists in list of boxes
                    boxes[(node[0] - 1, node[1])]\
                        .update({UP: path + [(node[0]-1, node[1])]})                #add UP and path to box's moves
                else:
                    boxes[(node[0] - 1, node[1])] \
                        = {UP: path + [(node[0]-1, node[1])]}                       #else add box to boxes
        else:
            neighbors.append((node[0] - 1, node[1]))                     #else add UP to neighbors

    ##DOWN##
    if board[node[0] + 1][node[1]] != WALL:                         #if DOWN is not a wall
        if board[node[0] + 1][node[1]] == BOX:                          #if DOWN is a box
            if board[node[0] + 2][node[1]] != WALL:                         #if you can push the box DOWN
                if (node[0] + 1, node[1]) in boxes:                             # if box exists in list of boxes
                    boxes[(node[0] + 1, node[1])]\
                        .update({DOWN: path + [(node[0]+1, node[1])]})              # add DOWN and path to box's moves
                else:
                    boxes[(node[0] + 1, node[1])] \
                        = {DOWN: path + [(node[0]+1, node[1])]}                     # else add box to boxes
        else:
            neighbors.append((node[0] + 1, node[1]))                    #else add DOWN to neighbors

    ##LEFT##
    if board[node[0]][node[1] - 1] != WALL:                         #if LEFT is not a wall
        if board[node[0]][node[1] - 1] == BOX:                          #if LEFT is a box
            if board[node[0]][node[1] - 2] != WALL:                         #if you can push the box LEFT
                if (node[0], node[1] - 1) in boxes:                             # if box exists in list of boxes
                    boxes[(node[0], node[1] - 1)]\
                        .udpate({LEFT: path + [(node[0], node[1]-1)]})              # add LEFT and path to box's moves
                else:
                    boxes[(node[0], node[1] - 1)] \
                        = {LEFT: path + [(node[0], node[1]-1)]}                     # else add box to boxes
        else:
            neighbors.append((node[0], node[1] - 1))                    #else add LEFT to neighbors

    ##RIGHT##
    if board[node[0]][node[1] + 1] != WALL:                         #if RIGHT is not a wall
        if board[node[0]][node[1] + 1] == BOX:                          #if RIGHT is a box
            if board[node[0]][node[1] + 2] != WALL:                         #if you can push the box RIGHT
                if (node[0], node[1] + 1) in boxes:                             # if box exists in list of boxes
                    boxes[(node[0], node[1] + 1)]\
                        .udpate({RIGHT: path + [(node[0], node[1]+1)]})             # add RIGHT and path to box's moves
                else:
                    boxes[(node[0], node[1] + 1)] \
                        = {RIGHT: path + [(node[0], node[1]+1)]}                    # else add box to boxes
        else:
            neighbors.append((node[0], node[1] + 1))                    #else add RIGHT to neighbors

    return neighbors, boxes

#
# TESTS
#
# FROM SOKOBAN INPUT FILES
# sokoban = sb.Sokoban("test/input/sokoban/sokoban00.txt")
# sokoban = sb.Sokoban("test/input/sokoban/sokoban01.txt")
# sokoban.print()
# agent = sb.Agent(sokoban.agentX, sokoban.agentY)
# boxes = getReachableBoxes(sokoban.board, agent)
# pprint.pprint(boxes)

# FROM TEXT LEVELS
# b = b.Board("test/input/levels/level0.txt")
b = b.Board("test/input/levels/level1.txt")
# b = b.Board("test/input/levels/level2.txt")
# b = b.Board("test/input/levels/level47.txt")
board = b.board
translation = {39: None}
print(str(board).translate(translation))
agent = sb.Agent(b.agentX, b.agentY)
boxes = getReachableBoxes(board, agent)
pprint.pprint(boxes)
# box = random.choice(list(boxes.items()))
# print(box)
# move = random.choice(list(box[1].keys()))
# box_move = {box[0]: move}
# print(box_move)

#GET NEXT ACTION TEST
# q_values = {}
# q_table = {(4, 7): {'Up': 1, 'Down': 2, 'Left': 3, 'Right': 4}}
# q_max = {}
# q_move = {}
# for box in boxes.keys():
#     if box not in q_table:
#         q_table[box] = {
#             UP: 0,
#             DOWN: 0,
#             LEFT: 0,
#             RIGHT: 0
#         }
#     q_values[box] = q_table[box]
# for box in q_values.keys():
#     max_move = max(q_values[box], key=q_values[box].get)
#     # q_max[box] = {max_move: q_values[box][max_move]}
#     q_move[box] = max_move
#     q_max[box] = q_values[box][max_move]
#
# box = max(q_max, key=q_max.get)
# box_move = {box: q_move[box]}
# print(q_values)
# print(q_max)
# print(q_move)
# print(box)
# print(box_move)
