import Board
def createState(board, vehicleNums):
    boards = []
    boards.append(board) #First element is the main vehicle 
    boards[0].current_pos = boards[0].start_pos
    for i in range(1, vehicleNums): 
        board_element = boards[i-1].copy()
        board_element.start_pos = board.find_start_pos(str(i))
        _start_pos = board_element.start_pos
        board_element.goal_pos = board.find_goal_pos(str(i))
        board_element.ID = i
        board_element.matrix[_start_pos[0]][_start_pos[1]] = 'S' + str(i)
        board_element.current_pos = _start_pos
        boards.append(board_element)
    return boards 

def restore_goal_positions(boards, board, numbervehicles):
    """
    Restore the start and goal positions for all vehicles on the board if they are not occupied.

    Args:
        boards: List of board objects for each vehicle.
        board: The board object representing the current state.
        numbervehicles: The total number of vehicles.
    """

    # Restore goal positions
    for vehicle_id in range(numbervehicles):
        goal_pos = boards[vehicle_id].goal_pos
        if goal_pos and board.matrix[goal_pos[0]][goal_pos[1]] == '0':
            board.matrix[goal_pos[0]][goal_pos[1]] = 'G' + str(vehicle_id)


def find_and_set_other_vehicles(board, current_vehicle_id):
    """
    Sets cells occupied by vehicles other than the one currently being processed to -1.

    Args:
        board: The Board object representing the environment.
        current_vehicle_id: The ID of the currently processed vehicle.

    Returns:
        None
    """
    for i in range(board.rows):
        for j in range(board.cols):
            cell_value = board.matrix[i][j]
            if cell_value == 'S': 
                vehicle_id = '0'  # Main vehicle ID
            elif cell_value.startswith('S'):
                vehicle_id = cell_value[1:]  # Extract vehicle ID from 'S{ID}'
            else:
                continue  # Skip non-vehicle cells
            
            # Set cell to -1 if it's occupied by another vehicle
            if vehicle_id != current_vehicle_id:
                board.matrix[i][j] = '-1'

def restore_vehicle_positions(boards, current_board):
    """
    Restores the positions of all vehicles to their original locations
    based on the recorded_start_goal.

    Args:
        boards: A list of Board objects representing the environments for multiple vehicles.

    Returns:
        None
    """
    for index, board in enumerate(boards):
        # Use recorded_start_goal to get the original position of each vehicle
        recorded_pos = board.current_pos
        
        if recorded_pos:
            # Restore the position in the matrix
            x, y = recorded_pos
            if board.ID == 0:
                current_board.matrix[x][y] = 'S'  # Main vehicle is represented as 'S'
            else:
                current_board.matrix[x][y] = f'S{board.ID}'  # Other vehicles are represented as 'S{ID}'
            # # Update the current position of the vehicle
            # board.current_pos = recorded_pos

    

def generateNewState(board, vehicle_id, gas_stations, moveto):
    print('gas stations:', gas_stations)
    if board.ID != vehicle_id:
        return None  # Return None if IDs don't match

    # Find the vehicle's current location
    if board.ID == 0:
        # For the main vehicle (ID 0), use the default find method
        vehicle_location = board.find_vehicle()
    else:
        # For other vehicles, use the vehicle_id as an argument
        vehicle_location = board.find_vehicle(str(vehicle_id))

    if vehicle_location is None:
        return None  # Handle the case where the vehicle is not found

    x_coord, y_coord = vehicle_location

    if moveto is None:
        # Convert the position the vehicle is staying to -1
        board.matrix[x_coord][y_coord] = '-1'
        board.time -= 1 
        board.recorded_move.append(None)
        return 
    else:
        new_x, new_y = moveto

        # Calculate the cost of the move
        move_cost = board.get_cost(new_x, new_y)

        if board.ID == 0:
            # Move main vehicle without changing start/goal positions
            board.move_vehicle(moveto)
            board.fuel -= 1  # Consume 1 fuel unit for the move
            board.time -= move_cost  # Subtract time cost for the move
            board.current_pos = (new_x, new_y)
        else:
            # Move other vehicles and check goal conditions
            board.move_vehicle(moveto, str(vehicle_id))
            board.fuel -= 1  # Consume 1 fuel unit for the move
            board.time -= move_cost  # Subtract time cost for the move
            board.current_pos = (new_x, new_y)
            # Check if the vehicle reached its goal
            vehicle_location = board.find_vehicle(str(vehicle_id))
            x_coord, y_coord = vehicle_location
            if x_coord == board.goal_pos[0] and y_coord == board.goal_pos[1]:
                board.delete_goal(str(vehicle_id))
                board.spawn_new_start(str(vehicle_id))
                board.spawn_new_goal(str(vehicle_id))
                return 
        # Check if the vehicle moved to a gas station
        if (gas_stations):
            if (new_x, new_y) in gas_stations: 
                board.fuel = board.inital_fuel  # Refill the fuel
        board.start_pos = moveto
    return board


def print_boards(boards):
    """Prints the information of each board in a list in a clear format.

    Args:
        boards (list): A list of boards, where each board is an object
                       with the attributes 'matrix', 'rows', 'cols',
                       'start_pos', 'goal_pos', 'time', and 'fuel'.
    """

    for i, board in enumerate(boards):
        print(f"Board {i+1}:")  # Print board number with 1-based indexing
        print(f"\tMatrix:")
        for row in board.matrix:
            print(f"\t\t{row}")  # Print each row of the matrix with indentation

        print(f"\tRows: {board.rows}")
        print(f"\tCols: {board.cols}")
        print(f"\tStart Position: {board.start_pos}")
        print(f"\tGoal Position: {board.goal_pos}")
        print(f"\t Initial Position: {board.current_pos}")
     #   print(f"\tTime: {board.time}")
       # print(f"\tFuel: {board.fuel}")
        print()  # Print an empty line for better readability between boards

def print_vehicle_status(board):
    """
    Prints the status of the vehicle including its index, remaining fuel, time, and current position.

    Args:
        board: The Board object representing the environment.
        vehicle_index: The index of the vehicle whose status is being printed.

    Returns:
        None
    """

    print(f"Vehicle Index: {board.ID}")
    print(f"Current Position: {board.current_pos}")
    # Optionally, print the state of the board
    board.print_board()
    print("\n")
    print(f"================================================================")