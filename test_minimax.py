"""
Test script to check for bugs in a minimax search,
and retrieve memory usage using guppy
"""
from boomers.player import Player,Node
import time
from guppy import hpy
from collections import Counter

h = hpy()

start = time.time()
begin = h.heap()

player = Player('black')
player.white.update({(1,1):0, (3,1):0, (4,1):0, (2,1):1, (4,3):1, (4,5):1})
player.black = Counter({(0, 7): 1, (1, 7): 1, (3, 7): 1, (4, 7): 1, (6, 7): 1, (7, 7): 1, (1, 6): 1, (6, 6): 1, (7, 6): 1, (0, 5): 1})
player.white = Counter({(1, 1): 1, (6, 1): 1, (7, 1): 1, (0, 0): 1, (1, 0): 1, (3, 0): 1, (4, 0): 1, (6, 0): 1, (7, 0): 1, (0, 2): 1})
player.black.update({(3,6):0, (4,6):0, (3,4):1, (3,2):1})

tree_root = Node(player)

player.expand_minimax_tree(tree_root, cutoff=2)
print(len(tree_root.children))

#Find the best move based from minimax leaf nodes
action = player.minimax_alpha_beta(tree_root)

mem = h.heap()-begin
print(action)
print(mem)
print("Operate time:",time.time()-start)