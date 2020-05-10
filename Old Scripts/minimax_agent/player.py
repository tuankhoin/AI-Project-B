import utils.functionality as func
import minimax_agent.config as config
from heuristics.search import nearest_opponent, euclidean, Node

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

        self.tree = None

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

        #Expand the minimax tree
        self.init_minimax()
        self.expand_minimax_tree(self.tree, cutoff=2)

        #Find the best move based from minimax leaf nodes
        action = self.minimax_alpha_beta()

        return action


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

        # Implementing suitable action update
        if action[0]=="MOVE":
            current_player, current_opponent = func.update_move(self, colour, action)
        else:
            current_player, current_opponent = func.update_boom(self, colour, action)

        self.player = current_player
        self.opponent = current_opponent

    def init_minimax(self):
        """
        Creates a minimax tree stump as Node object
        """
        self.tree = Node(None, None, self.color)
        self.tree.update_node_state(self.player, self.opponent)

    def expand_minimax_tree(self, node, cutoff=2):
        """
        Expands the minimax tree recursively until a certain depth, alternating between
        player and opponent actions

        Iterates over the player's tree object
        Minimax tree must be a stump and not None

        @params:
        cutoff: default=1, a positive int representing depth of tree to stop
                expansion
        """
        #Guard condition
        if cutoff <= 0:
            #Evaluate each node at the cutoff depth
            node.eval = self.evaluate(node)
            return

        #Expand the parent node first
        node.evaluate_actions()
        node.expand_all_minimax()

        #Expand each child for each node until cutoff reached
        for child in node.children.values():
            self.expand_minimax_tree(child, cutoff-1)

    def evaluate(self, curr_node):
        """
        Evaluates the leaf node's game state as advantageous for the player or
        Opponent

        ASSUMES MORE THAN 2-PLY SEARCH

        Considers symmetric score of:
        number of player tokens at the root node
        number of opponent tokens at root node
        number of player tokens at the leaf node
        number of opponent tokens at leaf node

        @params
        curr_node: a Node object, a leaf node of a minimax tree

        Returns an int representing the score of the action:
        positive int: advantageous towards player
        negative int: advantageous towards opponent
        """
        #Record the token counts for both colors at the root node
        start_opponent = func.get_total_tokens(self.tree.player.opponent)
        start_allies = func.get_total_tokens(self.tree.player.player)
        #Record token counts for both colors at leaf node
        opponent_count = func.get_total_tokens(curr_node.player.opponent)
        allies_count = func.get_total_tokens(curr_node.player.player)

        #Calculate the symmetric evaluation score
        score = (start_allies - start_opponent) \
                - (opponent_count - allies_count)

        return score

    def minimax_alpha_beta(self):
        """
        Finds the best action, using Alpha-Beta pruning, from an expanded
        minimax tree.

        ASSUMPTION:
        - minimax tree has been fully expanded to its leaf nodes

        Returns an action tuple of the best move
        """
        #Initialize [-infinity, infinity]
        alpha = float('-inf')
        beta = float('inf')
        best_action = None

        #Start alpha-beta search and expansion
        for child in self.tree.children.values():
            best_score = self.minimax_min(child, alpha, beta)

            print("\nNode: ", child, " has score: ", best_score)
            #If the value found after going down a branch is better, use the
            #value as the new alpha
            if best_score > alpha:
                alpha = best_score
                best_action = child.action_done

        return best_action

    def minimax_max(self, node, alpha, beta):
        """
        Finds the largest value in the leaf nodes for pruning alpha-beta

        @params:
        node: a Node object
        alpha, an int, representing the best value the algorithm has found
        beta, an int, representing the worst play's evaluation score

        Returns an int, score of the leaf node
        """

        #Check if the node is a leaf node
        if len(node.children) == 0:
            return node.eval

        #Init negative infinity for finding best score
        max_val = float('-inf')

        for child in node.children.values():
            max_val = max(max_val, self.minimax_min(child, alpha, beta))

            #Check if found a better move for player
            if max_val >= beta:
                return max_val
            else:
                alpha = max(max_val, alpha)

        return max_val

    def minimax_min(self, node, alpha, beta):
        """
        Finds the smallest value in the leaf nodes for pruning alpha-beta

        @params:
        node: a Node object
        alpha, an int, representing the best value the algorithm has found
        beta, an int, representing the worst play's evaluation score

        Returns an int, score of the leaf node
        """

        #Check if the node is a leaf node
        if len(node.children) == 0:
            return node.eval

        #Init negative infinity and infinity
        min_val = float('inf')

        for child in node.children.values():
            min_val = min(min_val, self.minimax_max(child, alpha, beta))

            #Check if found the worst move for player
            if min_val <= alpha:
                return min_val
            else:
                beta = min(min_val, beta)

        return min_val
