"""Run this script to test the newly implemented Node class functions"""
from boomers.player import Player,Node

player = Player('white')

node = Node(player)
print(node)

node.expand_all()
print(*node.children.items(), sep='\n')
print(len(node.children))

print(node.children[('MOVE', 1, (1,1), (0,1))])
