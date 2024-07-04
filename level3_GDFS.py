import heapq
from queue import Queue
from level1 import heuristic

def gbfs(board):
    start = board.start_pos
    goal = board.goal_pos
    initial_fuel = board.fuel
    gas_stations = board.find_gas_locations()

    stack = [(start, initial_fuel, [])]
    visited = set()

    while stack:
        (current_pos, fuel, path) = stack.pop()
        if current_pos == goal:
            return path + [current_pos]
        if (current_pos, fuel) in visited:
            continue
        visited.add((current_pos, fuel))

        # Explore neighbors
        neighbors = board.get_neighbors(current_pos)
        print(neighbors)
        for neighbor in neighbors:
            x, y = neighbor
            new_fuel = fuel - 1 if board.is_valid_move(x, y) else fuel
            if new_fuel < 0:
                continue
            # Refuel at gas stations
            if board.matrix[x][y][0] == 'F':
                new_fuel = initial_fuel  # refuel to full capacity
            new_path = path + [current_pos]
            stack.append((neighbor, new_fuel, new_path))
        
        # Sort stack based on heuristic distance to the goal
        #stack.sort(key=lambda node: heuristic(node[0], goal))

    return None  # No path found
