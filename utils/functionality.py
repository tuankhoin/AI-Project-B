from boomers.player import ExamplePlayer as Player

def get_available_action(player):
    """Returns a list that contains the available moves of a player"""
    action_list = []
    stack_list = player.player + player.opponent
    for stack in stack_list:
        stack = (stack[1],stack[2])

    for token in player.player:
        action_list.append(('BOOM', (token[1],token[2])))

        for i in range(token[1]-token[0], token[1]+token[0]+1):
            if i == token[1] or i<0 or i>7:
                continue
            if (i,token[2]) not in stack_list:
                for j in range(1, token[0]+1):
                    action_list.append(('MOVE', j, (token[1],token[2]), (i,token[2])))

        for i in range(token[2]-token[0], token[2]+token[0]+1):
            if i == token[1] or i<0 or i>7:
                continue
            if (i,token[1]) not in stack_list:
                for j in range(1, token[0]+1):
                    action_list.append(('MOVE', j, (token[1],token[2]), (token[1],i)))

    return action_list
