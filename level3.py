import heapq
from queue import Queue
from level1 import heuristic,reconstruct_path

def a_star_search(board, start, goal, initial_fuel):
    frontier = [(0, start, initial_fuel)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    fuel_at_node = {start: initial_fuel}

    while frontier:
        current_cost, current, fuel = heapq.heappop(frontier)

        if current == goal:
            return reconstruct_path(came_from, start, goal), cost_so_far[goal]

        for neighbor in board.get_neighbors(current):
            new_cost = cost_so_far[current] + board.get_cost(neighbor[0], neighbor[1])
            new_fuel = fuel - 1

            if board.matrix[neighbor[0]][neighbor[1]][0] == 'F':
                new_fuel = initial_fuel

            if new_fuel <= 0:
                continue

            if (neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]) and new_fuel >= 0:
                cost_so_far[neighbor] = new_cost
                fuel_at_node[neighbor] = new_fuel
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor, new_fuel))
                came_from[neighbor] = current

    return None, float('inf')

def A_star_search(board):
    start = board.start_pos
    goal = board.goal_pos
    initial_fuel = board.fuel
    gas_stations = board.find_gas_locations()

    if not start or not goal:
        return None

    # First, try to find a path directly from start to goal with the initial fuel
    path, total_cost = a_star_search(board, start, goal, initial_fuel)
    if path:
        return path

    # If not enough fuel, try to find the shortest path via gas stations
    shortest_path = None
    shortest_cost = float('inf')

    for gas_station in gas_stations:
        # Path from start to gas station
        path_to_gas, cost_to_gas = a_star_search(board, start, gas_station, initial_fuel)
        if not path_to_gas:
            continue

        # Path from gas station to goal after refueling
        path_from_gas, cost_from_gas = a_star_search(board, gas_station, goal, initial_fuel)
        if not path_from_gas:
            continue

        # Combine both paths and costs
        total_path = path_to_gas + path_from_gas[1:]  # Avoid duplicating the gas station in the path
        total_cost = cost_to_gas + cost_from_gas

        if total_cost < shortest_cost:
            shortest_path = total_path
            shortest_cost = total_cost

    return shortest_path if shortest_path else None



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
