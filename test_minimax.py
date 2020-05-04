from minimax_agent.player import ExamplePlayer as Player
import heuristics.search as s

#Have a white token at (0,5), in front of a black token (0,6)
test_player_list = white = [[1,0,5], [1,1,1],   [1,3,1], [1,4,1],   [1,6,1], [1,7,1],
         [1,0,0], [1,1,0],   [1,3,0], [1,4,0],   [1,6,0], [1,7,0]]

#Default black set up
black = [[1,0,7], [1,1,7],   [1,3,7], [1,4,7],   [1,6,7], [1,7,7],
         [1,0,6], [1,1,6],   [1,3,6], [1,4,6],   [1,6,6], [1,7,6]]

#Create a root node
root = s.Node(None, None, 'white')

#Create a player agent
player = Player('white')

#Change custom board layout if needed
root.update_node_state(test_player_list, black)

#Get all available actions
root.evaluate_actions()

#Creat children for root node
root.expand_all()

#Print moves and evaluated move scores
for poss_move in root.children:
    print("Move: ", poss_move)
    print("Score:", player.evaluate(root, poss_move), "\n")
