import sys
import heuristics.search as s
from boomers.player import ExamplePlayer as Player

node = s.Node(None,None,'white')
node.update_node_state([[2, 0, 1], [1, 1, 1], [1, 3, 1], [1, 4, 1],
                        [1, 6, 1], [1, 7, 1], [1, 0, 0], [1, 1, 0],
                        [1, 3, 0], [1, 4, 0], [1, 6, 0], [1, 7, 0]], 
                        node.player.opponent)
node.evaluate_actions()

print(node)

node.expand_all()

print(len(node.children))

child_node = node.expand(('MOVE', 1, (0,0), (0,1)))
print(child_node.player.player)
boom_node = node.expand(('BOOM', (1,1)))

"""print(child_node)
print(len(node.children))
print(node.actions)"""
print(node.player.player)
print(boom_node.player.player)

granchild_node = child_node.expand(('MOVE', 2, (0,1), (1,1)))
print(granchild_node.player.player)
print(granchild_node.propagate_back())