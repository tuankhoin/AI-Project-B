"""Run this script to test the newly implemented functions"""
from boomers.player import ExamplePlayer as Player
import utils.functionality as f

player = Player('white')
available = f.get_available_action(player)
clusters = f.get_clusters(player)
print(*available, sep='\n')
print(*clusters, sep='\n')

boom = ('BOOM', (0,0))
move1 = ('MOVE', 1, (7,0), (7,1))
move2 = ('MOVE', 1, (7,1), (7,0))

f.update_move(player, 'white', move1)

print(player)

f.update_boom(player, 'white', boom)

print(player)

f.update_move(player, 'white', move2)

print(player)
