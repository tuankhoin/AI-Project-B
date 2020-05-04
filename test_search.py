import sys
import heuristics.search as s
from boomers.player import ExamplePlayer as Player

# Create initial node
node = s.Node(None,None,'white')

# Update new initial node state
node.update_node_state([[2, 0, 1], [1, 1, 1], [1, 3, 1], [1, 4, 1],
                        [1, 6, 1], [1, 7, 1], [1, 0, 0], [1, 1, 0],
                        [1, 3, 0], [1, 4, 0], [1, 6, 0], [1, 7, 0]], 
                        node.player.opponent)

# Evaluate its actions
node.evaluate_actions()

print(node)
print(node.player.player)

# Expand all of it children
node.expand_all()

print(len(node.children))

# Manhattan and Euclidean
print(s.manhattan_upgraded(node.player.player[0], node.player.opponent[11]))
print(s.euclidean(node.player.player[0], node.player.opponent[11]))

# Making a child move node and boom node

boom_node = node.expand(('BOOM', (1,1)))
print("boomed's player:",boom_node.player.player)

child_node = node.expand(('MOVE', 1, (0,0), (0,1)))
print("child's player:",child_node.player.player)

# Testing chuld expansion and propagation to root action
granchild_node = child_node.expand(('MOVE', 2, (0,1), (1,1)))
print("granchild's player: ",granchild_node.player.player)
print("propagating granchild returns:",granchild_node.propagate_back())

# Testing minimax expansion
node = s.Node(None,None,'white')

# Update new initial node state
node.update_node_state([[2, 0, 1], [1, 1, 1], [1, 3, 1], [1, 4, 1],
                        [1, 6, 1], [1, 7, 1], [1, 0, 0], [1, 1, 0],
                        [1, 3, 0], [1, 4, 0], [1, 6, 0], [1, 7, 0]], 
                        node.player.opponent)

# Evaluate its actions
node.evaluate_actions()

print("node's player stack list:",node.player.player)

minimax_node = node.expand_minimax(('MOVE', 1, (0,0), (0,1)))
print(minimax_node)

node.children=[]
minimax_node.evaluate_actions()
minimax_node.expand_all_minimax()
print("Children of minimax_node:", len(minimax_node.children))

granchild_minimax = minimax_node.expand(('MOVE', 1, (0,7), (1,7)))
print(granchild_minimax)
print("Propagating granchild_minimax returns:", granchild_minimax.propagate_back())