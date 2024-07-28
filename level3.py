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

            if new_fuel == 0 and neighbor == goal:
                cost_so_far[neighbor] = new_cost
                fuel_at_node[neighbor] = new_fuel
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor, new_fuel))
                came_from[neighbor] = current
                continue


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
    if path and total_cost <= board.time:
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
        print(total_cost)
    return shortest_path if shortest_cost <= board.time else None



