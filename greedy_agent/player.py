from utils.functionality import get_available_action, update_move, update_boom
import heuristics.search as search
from copy import deepcopy

class ExamplePlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (White or Black). The value will be one of the
        strings "white" or "black" correspondingly.
        """
        # TODO: Set up state representation.
        self.color = colour
        self.player_prev = None
        self.opponent_prev = None
        # DEFAULT representation of a board: [ntoken, x, y]
        black = [[1,0,7], [1,1,7],   [1,3,7], [1,4,7],   [1,6,7], [1,7,7],
                 [1,0,6], [1,1,6],   [1,3,6], [1,4,6],   [1,6,6], [1,7,6]]
        white = [[1,0,1], [1,1,1],   [1,3,1], [1,4,1],   [1,6,1], [1,7,1],
                 [1,0,0], [1,1,0],   [1,3,0], [1,4,0],   [1,6,0], [1,7,0]]
        # allocating correct state representation of player and opponent
        if colour == 'white':
            self.player = white
            self.opponent = black
        else:
            self.player = black
            self.opponent = white
    def __str__(self):
        return "Player color: %s\n \
        Player stacks: %s\n \
        Opponent stacks: %s" % (self.color, self.player, self.opponent)


    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # TODO: Decide what action to take, and return it
        action_list = get_available_action(self)
        return search.greedy(self,action_list)


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action
        for the player colour (your method does not need to validate the action
        against the game rules).
        """
        # TODO: Update state representation in response to action.
        self.player_prev = deepcopy(self.player)
        self.opponent_prev = deepcopy(self.opponent)
                
        # Implementing suitable action update
        if action[0]=="MOVE":
            current_player, current_opponent = update_move(self, colour, action)
        else:
            current_player, current_opponent = update_boom(self, colour, action)

        self.player = current_player
        self.opponent = current_opponent
