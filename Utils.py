import Board
def createState(board, vehicleNums):
    boards = []
    boards.append(board) #First element is the main vehicle 
    for i in range(1, vehicleNums): 
        board_element = boards[i-1].copy()
        board_element.start_pos = board.find_start_pos(str(i))
        _start_pos = board_element.start_pos
        board_element.goal_pos = board.find_goal_pos(str(i))
        board_element.ID = i
        board_element.matrix[_start_pos[0]][_start_pos[1]] = 'S' + str(i)
        boards.append(board_element)
    return boards 

def generateNewState(board, vehicle_id, moveto):
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
    new_x, new_y = moveto

    # Calculate the cost of the move
    move_cost = board.get_cost_lv4(new_x, new_y, x_coord, y_coord)
    
    if board.ID == 0:
        # Move main vehicle without changing start/goal positions
        board.move_vehicle(moveto)
        board.fuel -= 1  # Consume 1 fuel unit for the move
        board.time -= move_cost  # Subtract time cost for the move

    else:
        # Move other vehicles and check goal conditions
        board.move_vehicle(moveto, str(vehicle_id))
        board.fuel -= 1  # Consume 1 fuel unit for the move
        board.time -= move_cost  # Subtract time cost for the move
        
        # Check if the vehicle reached its goal
        vehicle_location = board.find_vehicle(str(vehicle_id))
        x_coord, y_coord = vehicle_location
        if x_coord == board.goal_pos[0] and y_coord == board.goal_pos[1]:
            board.delete_goal(str(vehicle_id))
            board.spawn_new_start(str(vehicle_id))
            board.spawn_new_goal(str(vehicle_id))
    
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
        print(f"\tTime: {board.time}")
        print(f"\tFuel: {board.fuel}")
        print()  # Print an empty line for better readability between boards
