class Board:
    def __init__(self, matrix, time, fuel):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.start_pos = self.find_start_pos()
        self.goal_pos = self.find_goal_pos()
        self.time = time
        self.fuel = fuel
    def find_start_pos(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix[i][j] == 'S':
                    return (i, j)
        return None

    def find_goal_pos(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix[i][j] == 'G':
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
        elif cell_value.lower().startswith('f') and len(self.matrix[x][y]) > 1:
            return int(self.matrix[x][y][1:]) + 1  # parse the number following 'f'
        else:
            return int(cell_value) + 1  # assuming other cells contain string representation of an integer
