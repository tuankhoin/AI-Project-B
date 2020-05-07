import heuristics.search as s

# Testing minimax expansion
node = s.Node(None,None,'white')

# Update new initial node state
node.update_node_state([[2, 0, 1], [1, 1, 1], [1, 3, 1], [1, 4, 1],
                        [1, 6, 1], [1, 7, 1], [1, 0, 0], [1, 1, 0],
                        [1, 3, 0], [1, 4, 0], [1, 6, 0], [1, 7, 0]], 
                        node.player.opponent)

cutoff_list = node.null_move_search()

print(cutoff_list)