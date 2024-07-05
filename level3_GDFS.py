import heapq
from queue import Queue

def manhattan_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)

def gbfs(board):
    start = board.start_pos
    goal = board.goal_pos
    initial_fuel = board.fuel
    gas_stations = board.find_gas_locations()

    # Priority queue to store (heuristic, position, fuel, path)
    pq = []
    heapq.heappush(pq, (manhattan_distance(start, goal), start, initial_fuel, [start]))
    visited = set()

    best_path = None  # Initialize the best path found

    while pq:
        _, current_pos, fuel, path = heapq.heappop(pq)

        # Check if current position is the goal and path is viable
        if current_pos == goal and fuel >= manhattan_distance(current_pos, goal):
            print("Path found:", path)
            return path  # Return the path when goal is reached and reachable

        if (current_pos, fuel) in visited:
            continue

        visited.add((current_pos, fuel))

        for neighbor in board.get_neighbors(current_pos):
            x, y = neighbor
            new_fuel = fuel - 1  # Fuel decreases by 1 for each move
            if new_fuel < 0:
                continue

            if board.matrix[x][y][0].startswith('f') or board.matrix[x][y][0].startswith('F'):
                new_fuel = initial_fuel  # Refuel to full capacity
                new_path = path + [neighbor]
                new_distance = manhattan_distance(neighbor, goal)
                heapq.heappush(pq, (new_distance, neighbor, new_fuel, new_path))
            else:
                new_path = path + [neighbor]
                new_distance = manhattan_distance(neighbor, goal)
                heapq.heappush(pq, (new_distance, neighbor, new_fuel, new_path))

        # Update best_path if the current path is longer and valid
        if best_path is None or len(path) > len(best_path):
            best_path = path

    print("Best path found:", best_path)
    return best_path
