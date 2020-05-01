"""Include basic updating functions for the player"""

def update_move(player, color, action):
    """Updating the player status after a move action"""
    current_player = player.player
    current_opponent = player.opponent

    # Check if move is from opponent or player
    if player.color == color:
        list_update(action, current_player)
    else:
        list_update(action, current_opponent)
    return current_player, current_opponent



def list_update(action, stack_list):
    """Updating the status of the side that is on turn"""
    index = -1

    # Look for token in moved position
    for token in stack_list:
        if token[1] == action[2][0] and token[2] == action[2][1]:
            index = stack_list.index(token)
            break

    # Update or delete from list
    if action[1]==stack_list[index][0]:
        del stack_list[index]
    else:
        stack_list[index][0] -= action[1]

    # Look for token in moved destination
    destination_occupied = False
    for token in stack_list:
        if token[1] == action[3][0] and token[2] == action[3][1]:
            destination_occupied = True
            index = stack_list.index(token)
            break

    # Update or add to list
    if destination_occupied:
        stack_list[index][0] += action[1]
    else:
        stack_list.append([action[1], action[3][0], action[3][1]])


def update_boom(player, color, action):
    """Updating the player status after a boom action"""
    current_player = player.player
    current_opponent = player.opponent
    stacks = []
    destroyed_player = []
    destroyed_opponent = []
    destroyed_token = []

    # Which side ignited the boom?
    if color == player.color:
        stacks = current_player
    else:
        stacks = current_opponent

    # Chain up the boomed ones, strating from the ignition
    for token in stacks:
        if token[1] == action[1][0] and token[2] == action[1][1]:
            destroyed_token = token
            break
    cluster(player, destroyed_token, destroyed_player, destroyed_opponent)

    # Detonating
    for token in destroyed_player:
        current_player.remove(token)
    for token in destroyed_opponent:
        current_opponent.remove(token)

    return current_player, current_opponent

def cluster(player, destroyed_token, destroyed_player, destroyed_opponent):
    """Recursively adding adjacent stacks to the cluster lists"""
    # Recursive chaining to list for player stacks
    for token in player.player:
        if token not in destroyed_player and abs(token[1]-destroyed_token[1])<=1 and abs(token[2]-destroyed_token[2])<=1:
            destroyed_player.append(token)
            cluster(player, token, destroyed_player, destroyed_opponent)
    # Recursive chaining to list for opponent stacks
    for token in player.opponent:
        if token not in destroyed_opponent and abs(token[1]-destroyed_token[1])<=1 and abs(token[2]-destroyed_token[2])<=1:
            destroyed_opponent.append(token)
            cluster(player, token, destroyed_player, destroyed_opponent)
