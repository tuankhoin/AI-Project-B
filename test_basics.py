"""Run this script to test the newly implemented functions"""
from boomers.player import Player

player = Player('white')
#player.black[(2,4)] += 1
print(player)

available = player.get_available_action(False)
print(*available, sep='\n')

clusters = player.get_clusters()
print(*clusters, sep='\n')

boom = ('BOOM', (0,0))

move1=("MOVE", 1, (3,1), (4,1))
move2=("MOVE", 2, (4,1), (4,3))
move3=("MOVE", 1, (4,3), (4,5))
boom4 = ('BOOM', (4,5))

player.update('white', move1)
print(player)

player.update('white', move2)
print(player)

player.update('white', move3)
print(player)

print(player.closest())

available = player.get_available_action(False)
print(*available, sep='\n')

clusters = player.get_clusters()
print(*clusters, sep='\n')

#available = f.get_available_action(player)
#print(*available, sep='\n')

player.update('white', boom4)
print(player)

clusters = player.get_clusters()
print(*clusters, sep='\n')

print(player.evaluate())

