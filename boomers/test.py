"""Run this script to test the newly implemented functions"""
from player import ExamplePlayer as Player
from utils.update import update_move, update_boom

player = Player('white')

boom = ('BOOM', (0,0))
move = ('MOVE', 1, (7,0), (7,1))

update_move(player, 'white', move)

print(player)

update_boom(player, 'white', boom)

print(player)
