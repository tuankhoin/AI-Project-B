from minimax_agent.player import ExamplePlayer as Player
import heuristics.search as s

root = s.Node(None, None, 'white')

player = Player('white')

root.evaluate_actions()

root.expand_all()

for poss_move in root.children:
    print("Move: ", poss_move)
    print("Score:", player.evaluate(root, poss_move), "\n")
