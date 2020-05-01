"""Run this script to test the newly implemented functions"""
from boomers.player import ExamplePlayer as Player
from utils.update import update_move, update_boom

player = Player('white')

boom = ('BOOM', (0,0))
move1 = ('MOVE', 1, (7,0), (7,1))
move2 = ('MOVE', 1, (7,1), (7,0))

update_move(player, 'white', move1)

print(player)

update_boom(player, 'white', boom)

print(player)

update_move(player, 'white', move2)

print(player)
