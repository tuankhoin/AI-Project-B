from collections import Counter
from copy import deepcopy



BOOM_RADIUS = [(-1,+1), (+0,+1), (+1,+1),
               (-1,+0),          (+1,+0),
               (-1,-1), (+0,-1), (+1,-1)]

class Player:
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
        self.black = Counter({(0,7):1, (1,7):1,   (3,7):1, (4,7):1,   (6,7):1, (7,7):1,
                              (0,6):1, (1,6):1,   (3,6):1, (4,6):1,   (6,6):1, (7,6):1})
        self.white = Counter({(0,1):1, (1,1):1,   (3,1):1, (4,1):1,   (6,1):1, (7,1):1,
                              (0,0):1, (1,0):1,   (3,0):1, (4,0):1,   (6,0):1, (7,0):1})
        
        # allocating correct state representation of player and opponent
        self.turn = 0
        self.history = Counter({self.to_hash(): 1})
        
    def __str__(self):
        return "\tPlayer color: %s\tTurn: %d\n \
        Black stacks: %s\n \
        White stacks: %s\n" % (self.color, self.turn, self.black, self.white)


    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # TODO: Decide what action to take, and return it
        # Decide the first few moves to save up space and time
        if self.turn == 0 and self.color == 'white':
            return ("MOVE", 1, (3,1), (4,1))
        elif self.turn == 1 and self.color == 'black':
            return ("MOVE", 1, (4,6), (3,6))
        elif self.turn == 2 and self.color == 'white':
            return ("MOVE", 2, (4,1), (4,3))
        elif self.turn == 3 and self.color == 'black':
            return ("MOVE", 2, (3,6), (3,4))
        if self.turn == 4 and self.color == 'white':
            if self.black[(4,5)] == 0:
                return ("MOVE", 1, (4,3), (4,5))
        if self.turn == 5 and self.color == 'black':
            if self.white[(3,2)] == 0 and self.black[(3,4)] != 0:
                return ("MOVE", 1, (3,4), (3,2))
        return self.get_action()

    def get_action(self):
        #Expand the minimax tree
        tree_root = Node(self)
        self.expand_minimax_tree(tree_root, cutoff=2)

        #Find the best move based from minimax leaf nodes
        action = self.minimax_alpha_beta(tree_root)
        return action

    def expand_minimax_tree(self, node, cutoff=2):
        """
        Expands the minimax tree recursively until a certain depth, alternating between
        player and opponent actions

        Iterates over the player's tree object
        Minimax tree must be a stump and not None

        @params:
        cutoff: default=2, a positive int representing depth of tree to stop
                expansion
        """
        #Guard condition
        if cutoff <= 0:
            #Evaluate each node at the cutoff depth
            node.eval = node.evaluate()
            return

        #Expand the parent node first
        node.expand_all()

        #Expand each child for each node until cutoff reached
        for child in node.children.values():
            self.expand_minimax_tree(child, cutoff-1)

    def minimax_alpha_beta(self,tree):
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
        for child in tree.children.values():
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
        if action[0]=="MOVE":
            self.update_move(colour, action)
        else:
            self.update_boom(colour, action)

        self.turn += 1
        self.history[self.to_hash()] += 1

    def update_move(self, color, action):
        """Updating the player status after a move action"""
        # Check if move is from opponent or player
        if color == 'black':
            self.list_update(action, self.black)
        else:
            self.list_update(action, self.white)

    def list_update(self, action, stack_list):
        """Updating the status of the side that is on turn"""

        # Update or delete from list
        if action[1]==stack_list[action[2]]:
            del stack_list[action[2]]
        else:
            stack_list[action[2]] -= action[1]

        # Update new space
        stack_list[action[3]] += action[1]


    def update_boom(self, color, action):
        """Updating the player status after a boom action"""

        cluster_black = []
        cluster_white = []

        # Chain up the boomed ones, strating from the ignition
        self.cluster(action[1], cluster_black, cluster_white)

        # Detonating
        for black_pos in cluster_black:
            del self.black[black_pos]
        for white_pos in cluster_white:
            del self.white[white_pos]

    def cluster(self, position, cluster_black, cluster_white):
        """Recursively adding adjacent stacks to the cluster lists"""
        if self.black[position] != 0:
            cluster_black.append(position)
        elif self.white[position] != 0:
            cluster_white.append(position)

        # Recursive chaining to list for player stacks
        x,y = position
        for dx,dy in BOOM_RADIUS:
            if self.black[(x+dx, y+dy)] != 0 and (x+dx, y+dy) not in cluster_black:
                self.cluster((x+dx, y+dy), cluster_black, cluster_white)
            if self.white[(x+dx, y+dy)] != 0 and (x+dx, y+dy) not in cluster_white:
                self.cluster((x+dx, y+dy), cluster_black, cluster_white)

    def get_clusters(self):
        """Retrieve a list of clusters_array of type [clustered_player, clustered_opponent]
            cluster_array[0]: Array of black stacks in the cluster
            cluster_array[1]: Array of white stacks in the cluster"""
        clusters = []
        is_added = False

        # Iterate through each black position in the collection
        for pos in self.black:
            is_added = False
            # See if each created cluster contains the position yet
            for cluster_element in clusters:
                if pos in cluster_element[0]:
                    is_added = True
                    break
            # If not, append a new cluster to the list
            if not is_added:
                l = len(clusters)
                clusters.append([[],[]])
                self.cluster(pos, clusters[l][0], clusters[l][1])
        # Do the same for white positions
        for pos in self.white:
            is_added = False
            for cluster_element in clusters:
                if pos in cluster_element[1]:
                    is_added = True
                    break
            if not is_added:
                l = len(clusters)
                clusters.append([[],[]])
                self.cluster(pos, clusters[l][0], clusters[l][1])
        return clusters

    def get_total_tokens(self):
        """
        Counts the total number of tokens a given color has. Adds up each stack for
        the faction in question.

        Returns 2 positive ints, total number of tokens for black and white respectively
        """
        total_black = sum(self.black.values())
        total_white = sum(self.white.values())
        return total_black, total_white


    def get_opponent_color(self):
        """Return a player's opponent color"""
        if self.color == 'white':
            return 'black'
        elif self.color == 'black':
            return 'white'
        else:
            return None

    def get_available_action(self, is_black=True):
        """Returns a list that contains the available moves of a color, black by default \n
        Put False to argument to get action of whites"""
        action_list = []
        if is_black:
            player_list = self.black
            opponent_list = self.white
        else:
            player_list = self.white
            opponent_list = self.black

        # For each token on board:
        for pos in player_list:
            x, y = pos
            action_list.append(('BOOM', pos))

            # Check for all available horizontal moves
            num_tokens = player_list[pos]
            for i in range(x-num_tokens, x+num_tokens+1):
                # Out bound/null move checking
                #print(i,y)
                if i == x or i<0 or i>7:
                    continue
                # Check if space is occupied by rival's stack
                if (i,y) not in opponent_list:
                    # All available moves in range
                    for j in range(1, num_tokens+1):
                        action_list.append(('MOVE', j, pos, (i,y)))

            # Check for all available vertical moves
            for i in range(y-num_tokens, y+num_tokens+1):
                if i == y or i<0 or i>7:
                    continue
                if (x,i) not in opponent_list:
                    for j in range(1, num_tokens+1):
                        action_list.append(('MOVE', j, pos, (x,i)))
        return action_list

    def to_hash(self):
        """Returns the hash value of state to store in the transposition table
        Idea taken from Zobrist Hashing and referee.game"""
        return (
            tuple((pos,n) for pos,n in sorted(self.white.items())+sorted(self.black.items())), 
            self.turn % 2,
        )

    def evaluate(self):
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

        """
        #Record the token counts for both colors at the root node
        start_opponent = self.get_total_tokens(self.color == 'white')
        start_allies = self.get_total_tokens(self.color == 'black')
        #Record token counts for both colors at leaf node
        opponent_count = self.get_total_tokens(curr_node.player.opponent)
        allies_count = self.get_total_tokens(curr_node.player.player)

        #Calculate the symmetric evaluation score
        score = (start_allies - start_opponent) \
                - (opponent_count - allies_count)
        """
        score = 0
        return score

class Node:
    """Each node will contains a player's state and its available moves: \n
        depth: node depth. Initial node is 0 in depth \n
        action_done: resulted action that create the node, null if first \n
        parent: its predecessor state, null if first \n
        children: its list of following steps \n
        player: its representing game state \n
        eval: evalutation function result of node \n
        table: the transposition table to detect repeated states \n
        """
    def __init__(self, player):

        self.player = player

        self.parent = None
        self.action_done = None

        # depth % 2 == 0 : Player in turn (max)
        # depth % 2 != 0 : Opponent in turn (min)
        self.depth = 0

        # children and actions: Only generated upon expanding
        self.children = {}
        self.eval = 0

        # transposition table
        self.table = Counter()
        self.table.update(self.player.history)

    def __str__(self):
        return "\tResulted from: %s\n\
        Depth: %d \t Player color: %s\n\
        Black stacks: %s\n\
        White stacks: %s\n" % (self.action_done, self.depth, self.player.color, self.player.black, self.player.white)

    def expand(self, color, action):
        """Expand each action to a child node for use in minimax"""
        child = Node(deepcopy(self.player))

        child.player.update(color, action)
        child.player.color = self.player.get_opponent_color()
        child.parent = self
        child.action_done = action
        child.depth = self.depth + 1

        # Only append to tree if the new child does not repeat any state
        child_hash_key = child.player.to_hash()
        if not self.table[child_hash_key]:
            self.children[action] = child
            self.table[child_hash_key] += 1

    def expand_all(self):
        """Expanding all available actions into children nodes for minimax"""
        actions = self.player.get_available_action(self.player.color == 'black')

        for action in actions:
            self.expand(self.player.color,action)

    def propagate_back(self):
        """Return the original node's action that resulted in this node"""
        root = self.parent
        while root.parent.parent != None:
            root = root.parent
        return root.action_done

    def evaluate(self):
        """Evaluate function of a node"""
        return self.player.evaluate() + 0


    



