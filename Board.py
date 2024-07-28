import random

class Board:
    def __init__(self, matrix, time, fuel):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.start_pos = self.find_start_pos()
        self.goal_pos = self.find_goal_pos()
        self.time = time
        self.fuel = fuel
        self.ID = 0
        self.inital_fuel = fuel 
        self.recorded_move = []
        self.recorded_start_goal = {} 
        self.current_pos = None 
    def find_start_pos(self, vehicle = ''):
        #default find G
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix[i][j] == 'S' + vehicle:
                    return (i, j)
        return None

    def find_goal_pos(self, vehicle = ''):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix[i][j] == 'G' + vehicle:
                    return (i, j)
        return None
    
    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if self.is_valid_move(new_x, new_y):
                neighbors.append((new_x, new_y))
        return neighbors
    
    # def is_valid_move(self, x, y):
    #         print("is_valid_move:", self.ID, "x:", x, "y:", y, "value:", self.matrix[x][y] if )
    #         return 0 <= x < self.rows and 0 <= y < self.cols and (self.matrix[x][y] != '-1' and not self.matrix[x][y].startswith('S'))
            
    def is_valid_move(self, x, y):
            return 0 <= x < self.rows and 0 <= y < self.cols and self.matrix[x][y] != '-1'

    def find_gas_locations(self):
        gas_stations = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix[i][j][0].startswith('F'): 
                    gas_stations.append((i,j))
        if gas_stations:
            return gas_stations
        return None
    
    def get_cost(self, x, y):
        cell_value = self.matrix[x][y][0]
        if cell_value in ['G', 'S', '0', '-1']:
            return 1
        elif cell_value.startswith('F') and len(self.matrix[x][y]) > 1:
            return int(self.matrix[x][y][1:]) + 1  # parse the number following 'f'
        else:
            return int(cell_value) + 1  # assuming other cells contain string representation of an integer

    def delete_goal(self, vehicle):
        #delete vehicle's goal
        #vehicle: string from "1" to "9"
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix[i][j] == 'S' + vehicle:  # Check if the cell is empty
                    self.matrix[i][j] = '0'
                    self.goal_pos = None 
        return None

    def spawn_new_start(self,vehicle):
         #spawn new goal for other vehicles
        #vehicle: string from "1" to "9"
        available_positions = []
        new_start_pos = self.current_pos
        self.record_start_and_goal(new_start_pos, None)
        self.start_pos = new_start_pos
        self.current_pos = new_start_pos
        self.recorded_move.append(new_start_pos)
        return new_start_pos

    
    def spawn_new_goal(self, vehicle):
        #spawn new goal for other vehicles
        #vehicle: string from "1" to "9"
        available_positions = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix[i][j] == '0':  # Check if the cell is empty
                    available_positions.append((i, j))
        
        if available_positions:
            new_goal_pos = random.choice(available_positions)
            self.matrix[new_goal_pos[0]][new_goal_pos[1]] = 'G' + vehicle
            self.record_start_and_goal(None, new_goal_pos)
            self.goal_pos = new_goal_pos
            return new_goal_pos
        return None

    def print_board(self):
        for row in self.matrix:
            print(' '.join(row))
            
    def find_vehicle(self, vehicle = ''):
        #default find S
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix[i][j] == 'S' + vehicle:
                    return (i, j)
        return None
    
    def move_vehicle(self, move_to, vehicle = ''):
        #move vehicle
        #vehicle: string from "0" to "9" default is for S
        #current and move_to: (x,y)value
        x, y = self.find_vehicle(vehicle)
        if (not self.is_valid_move(move_to[0], move_to[1])): 
            print("Id not move:", self.ID)
            return None
        self.matrix[x][y] = '0'
        self.matrix[move_to[0]][move_to[1]] = 'S' + vehicle
        self.recorded_move.append(move_to)

        
    def copy(self):
        """Creates a deep copy of the Board object.

        Returns:
            A new Board object with a copy of the original board's data.
        """

        # Deep copy the matrix using list comprehension
        new_matrix = [[cell for cell in row] for row in self.matrix]

        # Create a new Board object with copied data
        return Board(new_matrix, self.time, self.fuel)
    
    def record_start_and_goal(self, start_pos=None, goal_pos=None):
        """
        Records the start and goal positions for a vehicle.
        """
        if start_pos:
            self.recorded_start_goal[start_pos] = goal_pos
        elif goal_pos:
            for start in self.recorded_start_goal:
                if self.recorded_start_goal[start] is None:
                    self.recorded_start_goal[start] = goal_pos
                    break


      

        