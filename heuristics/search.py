""" This is the collection package of search utilities and heuristic
    functions to apply on agents that use heuristics 
    Goal: Find a space that brings the most opponent cluster"""


"""Node functionality evaluation"""

def nearest_opponent(player, token):
    pass

def get_direct_cost(action):
    return 0

def get_heuristics(action):
    return 0

"""Search algorithms"""

def greedy(action_list):
    """Using the greedy algorithm, choose the best action
    from the list of available moves"""
    best_action = action_list[0]
    best_cost = 0

    for action in action_list:
        cost = get_direct_cost(action) + get_heuristics(action)
        if cost > best_cost:
            best_action = action
            best_cost = cost
    return best_action

