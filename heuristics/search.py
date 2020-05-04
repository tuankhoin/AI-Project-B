""" This is the collection package of search utilities and heuristic
    functions to apply on agents that use heuristics 
    Goal: Find a space that brings the most opponent cluster"""
import math
from copy import deepcopy
import utils.functionality as f
from boomers.player import ExamplePlayer as Player

class Node:
    """Each node will contains a player's state and its available moves:
        parent: its predecessor state
        children: its following steps
        actions: its available actions
        player: its representing game state
        g(x) + h(x) = cost(x)
        """
    def __init__(self, parent, action, color):

        self.player = Player(color)

        self.parent = parent
        self.action_done = action
        if parent != None:
            self.player.color = self.parent.player.color
            self.player.player = deepcopy(parent.player.player)
            self.player.opponent = deepcopy(parent.player.opponent)
            self.player.update(self.player.color, action)
        self.children = []

        self.actions = None
        self.g = 0
        self.h = 0

    def evaluate_actions(self):
        """Only retrieve the necessary actions when needed, to save space"""
        self.actions = f.get_available_action(self.player)
    
    def expand(self,action):
        """Returns the resulted children from applying action"""
        for child in self.children:
            if child.action_done == action:
                return child
        new_child = Node(self, action, self.player.color)
        self.children.append(new_child)
        return new_child

    def expand_all(self):
        """Expand all of a node's children"""
        for action in self.actions:
            self.children.append(Node(self, action, self.player.color))

    def propagate_back(self):
        """Return the original node's action that resulted in this node"""
        root = self.parent
        while root.parent.parent != None:
            root = root.parent
        return root.action_done

    def update_node_state(self, player_list, opponent_list):
        """By default the initial node created will represent the default board state.
        This function is used to update the true state to the node
        WARNING: Only use this on the initial node created"""
        self.player.player = player_list
        self.player.opponent = opponent_list

"""Node functionality evaluation"""

def nearest_opponent(player, token):
    """Return the closest opponent's stack to the argument token"""
    closest_sum = 999
    closest_opponent = None
    for rival in player.opponent:
        sum = euclidean(token, rival)
        if sum < closest_sum:
            closest_opponent = rival
            closest_sum = sum
    return closest_opponent

def get_distance(token_one, token_two):
    """Returns x and y distance between 2 token stacks"""
    return abs(token_one[1]-token_two[1]), abs(token_one[2]-token_two[2])

def euclidean(token_one, token_two):
    """Returns the euclidean distance between two tokens"""
    x, y = get_distance(token_one,token_two)
    return math.sqrt(x**2+y**2)

def manhattan_upgraded(token_one, token_two):
    """Return the upgraded manhattan distance for getting from token_one to token_two"""
    x, y = get_distance(token_one,token_two)
    return math.floor((x+y)/token_one[0])

def get_direct_cost(player,action):
    return 0

def get_heuristics(player,action):
    if action[0]=='BOOM':
        pass
    else:
        x_move, y_move = action[3]
        move_token = f.get_token_position(player, action[2])
        closest_opponent = nearest_opponent(player, move_token)
        return euclidean([1, x_move, y_move],closest_opponent)-euclidean(move_token, closest_opponent)
    return 0

"""Search algorithms"""

def greedy(player,action_list):
    """Using the greedy algorithm, choose the best action
    from the list of available moves"""
    best_action = action_list[0]
    best_cost = 0

    for action in action_list:
        cost = get_direct_cost(player,action) + get_heuristics(player,action)
        if cost > best_cost:
            best_action = action
            best_cost = cost
    return best_action

def a_star(action_list):
    pass

