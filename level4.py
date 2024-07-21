import heapq
from queue import Queue
from Utils import createState
from level1 import reconstruct_path 
from Utils import createState, generateNewState, print_boards
def heuristic(pos, goal):
  """
  Calculates the Manhattan distance heuristic between two positions.

  Args:
      pos: Starting position (tuple of x, y coordinates).
      goal: Goal position (tuple of x, y coordinates).

  Returns:
      The Manhattan distance between the positions.
  """

  x1, y1 = pos
  x2, y2 = goal
  return abs(x1 - x2) + abs(y1 - y2)

def is_occupied_by_other_vehicle(cell, paths, current_vehicle):
  """
  Checks if a cell is occupied by another vehicle (excluding the current vehicle).

  Args:
      cell: The position to check (tuple of x, y coordinates).
      paths: List of paths for all vehicles.
      current_vehicle: Index of the currently processed vehicle (0-based).

  Returns:
      True if the cell is occupied by another vehicle, False otherwise.
  """

  for i, path in enumerate(paths):
    if i != current_vehicle and path is not None and cell in path:
      return True
  return False


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

def A_star_search(board, goal, initial_fuel, gas_stations):
    start = board.start_pos
    print("board start pos:", board.start_pos)
    print("board goal pos:", goal)
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

def A_star_search_lv4(boards):
    """
    Performs A* search for multiple vehicles on separate boards with turn-based movement,
    handling collision avoidance and Level 4 cost calculations. The loop continues until
    the main vehicle reach its goal 'G'.

    Args:
        boards: A list of Board objects, each representing the environment for a vehicle.

    Returns:
        A list of paths, one for each vehicle (may contain None if no path is found).
    """

    paths = [None] * len(boards)  # Initialize list to store paths for each vehicle
    vehicle_paths = [[] for _ in boards]  # Store the planned path for each vehicle
    gas_stations = boards[0].find_gas_locations()

    while True:
        main_vehicle_location = boards[0].find_vehicle()
        x_coord, y_coord = main_vehicle_location
        if x_coord == boards[0].goal_pos[0] and y_coord == boards[0].goal_pos[1]:
            break

        # Update and pass board state between vehicles
        for vehicle_index in range(len(boards)):
            board = boards[vehicle_index]
            initial_fuel = board.fuel
            goal_pos = board.goal_pos
            if not vehicle_paths[vehicle_index]:
                # Plan a new path if there's no current path
                path = A_star_search(board, goal_pos, initial_fuel, gas_stations)
                if path is None:
                    print(f"Vehicle {vehicle_index} cannot find a path to the goal.")
                    return paths
                vehicle_paths[vehicle_index] = path

            # Execute one step of the path
            if vehicle_paths[vehicle_index]:
                move_to = vehicle_paths[vehicle_index].pop(0)
                generateNewState(board, vehicle_index, move_to)
                paths[vehicle_index] = vehicle_paths[vehicle_index]

                # Print the state of the board after the move
                print("================================================================")
                print(f"Vehicle Index: {vehicle_index}")
                print(f"Move To: {move_to}")
                print(f"Fuel Remaining: {board.fuel}")
                print(f"Time: {board.time}")
                print("State of the board after one step:")
                board.print_board()
                print("\n")
                print("================================================================")

                # Pass the updated state to the next vehicle
                if vehicle_index < len(boards) - 1:
                    #new_board = board.copy()
                    # print("================================================================")
                    # new_board.print_board()
                    boards[vehicle_index + 1].matrix = board.matrix 

                # Re-check the main vehicle's position after every move
                main_vehicle_location = boards[0].find_vehicle()
                x_coord, y_coord = main_vehicle_location
                if x_coord == boards[0].goal_pos[0] and y_coord == boards[0].goal_pos[1]:
                    break

    return paths
