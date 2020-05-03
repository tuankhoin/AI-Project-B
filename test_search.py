import heuristics.search as s
from boomers.player import ExamplePlayer as Player

node = s.Node(None,None,'white')

print(node)

node.expand_all()

print(len(node.children))

child_node = node.expand(('MOVE', 1, (0,0), (0,1)))
boom_node = node.expand(('BOOM', (1,1)))

print(child_node)
print(len(node.children))
print(node.actions)