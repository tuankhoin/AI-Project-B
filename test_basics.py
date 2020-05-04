"""Run this script to test the newly implemented functions"""
from boomers.player import ExamplePlayer as Player
import utils.functionality as f

player = Player('white')
available = f.get_available_action(player)
clusters = f.get_clusters(player)
print(*available, sep='\n')
print(*clusters, sep='\n')

boom = ('BOOM', (0,0))

move1=("MOVE", 1, (3,1), (4,1))
move2=("MOVE", 2, (4,1), (4,3))
move3=("MOVE", 1, (4,3), (4,5))

f.update_move(player, 'white', move1)
f.update_move(player, 'white', move2)
f.update_move(player, 'white', move3)

print(player)

available = f.get_available_action(player)
opponent = f.get_opponent_action(player)

print(*available, sep='\n')
print(*opponent,  sep='\n')

f.update_boom(player, 'white', boom)

print(player)


