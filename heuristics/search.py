""" This is the collection package of search utilities and heuristic
    functions to apply on agents that use heuristics 
    Goal: Find a space that brings the most opponent cluster"""
import math
from copy import deepcopy
import utils.functionality as f
from boomers.player import ExamplePlayer as Player

class Node:
    """Each node will contains a player's state and its available moves: \n
        depth: node depth. Initial node is 0 in depth \n
        action_done: resulted action that create the node, null if first \n
        parent: its predecessor state, null if first \n
        children: its list of following steps \n
        actions: its available actions \n
        player: its representing game state \n
        eval: evalutation function result of node \n
        """
    def __init__(self, parent, action, color):

        self.player = Player(color)

        self.parent = parent
        self.action_done = action
        if parent != None:
            self.depth = self.parent.depth + 1
            self.player.color = self.parent.player.color
            self.player.player = deepcopy(parent.player.player)
            self.player.opponent = deepcopy(parent.player.opponent)
            self.player.update(self.player.color, action)
        else:
            self.depth = 0

        self.children = dict()
        self.actions = None
    def __str__(self):
        return "\tResulted from: %s\n\
        Depth: %d \t Player color: %s\n\
        Player stacks: %s\n\
        Opponent stacks: %s\n" % (self.action_done, self.depth, self.player.color, self.player.player, self.player.opponent)

    def evaluate_actions(self):
        """Only retrieve the necessary actions when needed, to save space"""
        self.actions = f.get_available_action(self.player)

    def evaluate(self):
        """Node's evaluation function"""
        return 0

    def expand(self,action):
        """Returns the resulted children from applying action"""
        if action in self.children:
            return self.children[action]
        new_child = Node(self, action, self.player.color)
        self.children[action] = new_child
        return new_child

    def expand_minimax(self, action):
        """Returns the resulted children from applying action. 
            For use in minimax to switch turns"""
        if action in self.children:
            return self.children[action]
        new_child = Node(self, action, self.player.color)
        swap_turn(new_child)
        self.children[action] = new_child
        return new_child

    def expand_all(self):
        """Expand all of a node's children\n
        #WARNING: need to evaluate_actions first if you are using this, or it will return none"""
        for action in self.actions:
            self.children[action] = Node(self, action, self.player.color)

    def expand_all_minimax(self):
        """Expand all of a node's children, with turn swapping for minimax\n
        #WARNING: need to evaluate_actions first if you are using this, or it will return none"""
        for action in self.actions:
            child = Node(self, action, self.player.color)
            swap_turn(child)
            self.children[action] = child

    def expand_null_move(self):
        """Expand the node for case of null move"""    
        swap_turn(self)
        self.evaluate_actions()

        self.expand_all_minimax()

        # Reswap to make the node go back to normal
        swap_turn(self)
        self.actions = []

    def propagate_back(self):
        """Return the original node's action that resulted in this node"""
        root = self.parent
        while root.parent.parent != None:
            root = root.parent
        return root.action_done

    def update_node_state(self, player_list, opponent_list):
        """By default the initial node created will represent the default board state.\n
        This function is used to update the true state to the node\n
        # WARNING: Only use this on the initial node created"""
        self.player.player = player_list
        self.player.opponent = opponent_list

    def arrange_actions(self, first_to_expand):
        """From a given list of nodes that should be expanded first, rearrange them to the first of the list"""
        for action in first_to_expand:
            self.actions.remove(action)
            self.actions.insert(0, action)

    def null_move_search(self):
        """Do a shallow minimax search on the depth of 2, return a list of nodes that produces cutoffs"""
        cutoffs = dict()
        beta = -math.inf
        self.expand_null_move()
        curr_action = None

        # Expanding each child
        for ch in self.children.values():
            ch.evaluate_actions()
            ch.expand_all_minimax()
            min_value = math.inf
            is_cutoff = False

            # Evaluate for each granchildren
            for granchild in ch.children.values():
                val = granchild.evaluate()
                # Update the minimum value for child
                print(val,min_value,beta)
                if val < min_value:
                    min_value = val
                    # If min_value is less than beta, leave the rest. The previous child node has produced a cutoff
                    if min_value < beta:
                        is_cutoff = True
                        break
            
            # If current child got cut off, the previous child produced it
            if is_cutoff:
                if ch.action_done not in cutoffs:
                    cutoffs[ch.action_done] = True
            else:
                # Update what the previous child is
                curr_action = ch.action_done
                beta = min_value
        
        return cutoffs


"""Node functionality evaluation"""
def create_init_node(player):
    """Initialize a node for searching from the player's state"""
    node = Node(None,None,player.color)
    node.update_node_state(player.player, player.opponent)
    return node

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
    """Greedy cost: player_loss_tokens - opponent_loss_tokens"""
    if action[0] == 'BOOM':
        player_copy = deepcopy(player)
        boom_player, boom_opponent = f.update_boom(player_copy, player.color, action)
        #boom_player, boom_opponent = f.update_boom(player, player.color, action)
        total_token_player, total_token_opponent = f.get_total_tokens(boom_player), f.get_total_tokens(boom_opponent)
        #print(total_token_player,total_token_opponent)
        total_past_player, total_past_opponent = f.get_total_tokens(player.player), f.get_total_tokens(player.opponent)
        #print(total_past_player,total_past_opponent)
        delta_player = total_token_player - total_past_player
        delta_opponent = total_token_opponent - total_past_opponent
        return delta_opponent - delta_player
    else:
        return 0

def get_heuristics(player,action):
    """Greedy heuristics: The smallest step size to boom an opponent token"""
    if action[0]=='BOOM':
        return 0
    else:
        move_token = f.get_token_position(player, action[2])
        closest_opponent = nearest_opponent(player, move_token)
        return manhattan_upgraded(move_token, closest_opponent)

"""Search algorithms"""

def greedy(player,action_list):
    """Using the greedy algorithm, choose the best action
    from the list of available moves"""
    best_action = action_list[0]
    best_cost = 999

    for action in action_list:
        #print(get_direct_cost(player, action),get_heuristics(player,action))
        cost = 1.5*get_direct_cost(player, action) + get_heuristics(player,action)
        #print(cost, best_cost)
        if cost < best_cost:
            best_action = action
            best_cost = cost
    return best_action

def minimax(player):
    node = create_init_node(player)
    node.evaluate_actions()
    pass

def swap_turn(node):
    """Swap positions when needed to evaluate points from opponent's perspective,
        or reswap when need to return to the player's turn"""
    pointer = node.player.player
    node.player.player = node.player.opponent
    node.player.opponent = pointer
    node.player.color = f.get_opponent_color(node.player)


