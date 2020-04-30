"""Include basic updating functions for the player"""
def update_move(player, color, action):
    current_player = player.player
    current_opponent = player.opponent

    # Check if move is from opponent or player
    if player.color == color:
        list_update(action, current_player)
    else:
        list_update(action, current_opponent)
    return current_player, current_opponent

def update_boom(player, color, action):
    current_player = [[1,0,7], [1,1,7],   [1,3,7], [1,4,7],   [1,6,7], [1,7,7],
                      [1,0,6], [1,1,6],   [1,3,6], [1,4,6],   [1,6,6], [1,7,6]]
    current_opponent = [[1,0,1], [1,1,1],   [1,3,1], [1,4,1],   [1,6,1], [1,7,1],
                        [1,0,0], [1,1,0],   [1,3,0], [1,4,0],   [1,6,0], [1,7,0]]
    return current_player, current_opponent

def list_update(action, stack_list):
    ntoken = 1
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
