import heapq
from queue import Queue

def reconstruct_path(came_from, start, goal):
    if goal not in came_from:
        return None
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def heuristic(a, b):
    #Count distance between 2 points
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def BFS(board):
    #Breadth-First-Search
    '''
    Parameters
    ----------
    board: <class Board type> contain matrix and utility function
    Returns
    -------
    List of valid paths
    -------
    Below functions will have the same paramenters and reuturn
    '''
    queue = Queue()
    start=board.start_pos
    goal=board.goal_pos
    if not start or not goal:
        return None
    queue.put(start)
    visited = set()
    path = {start: [start]}
    #came_from = {start: None}

    while not queue.empty():
        current = queue.get()
        if current == goal:
            return path[current]
            #return reconstruct_path(came_from, start, goal)
        if current not in visited:
            visited.add(current)
            neighbor=board.get_neighbors(current)
            for pos in neighbor:
                queue.put(pos)
                if (pos) not in path:
                    path[pos] = path[current] + [pos]
                    #came_from[pos]=current
    return None

def DFS(board):
    '''Depth-First-Search
    '''
    start = board.start_pos
    goal = board.goal_pos
    if not start or not goal:
        return None 
    
    # Initialize the stack with the starting position
    stack = [start]
    # Set to keep track of visited nodes
    visited = set()
    path = {start: [start]}
    while stack:
        # Pop a node from the stack
        current = stack.pop()
        if current == goal:
            return path[current]  # Return the path to the goal

        if current not in visited:
            visited.add(current)  # Mark the current node as visited
            # Get the neighbors of the current node
            neighbors = board.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)
                    if neighbor not in path:
                        # Update the path to this neighbor
                        path[neighbor] = path[current] + [neighbor]

    return None  
def UCS(board):
    '''Uniform-Cost Search'''
    start = board.start_pos
    goal = board.goal_pos
    if not start or not goal:
        return None

    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current_cost, current = heapq.heappop(frontier)

        if current == goal:
            return reconstruct_path(came_from, start, goal)

        for neighbor in board.get_neighbors(current):
            new_cost = cost_so_far[current] + 1  # Assuming each move costs 1 unit
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heapq.heappush(frontier, (new_cost, neighbor))
                came_from[neighbor] = current

    return None


def IDS(board):
    '''Iterative deepening search
    '''
    depth_limit = 0
    while True:
        result = DLS(board, depth_limit)
        if result is not None:
            return result
        depth_limit += 1  # Increase depth limit for next iteration

    return None

def GBFS(board):
    '''Greedy Best First Search
    '''
    start=board.start_pos
    goal=board.goal_pos
    if not start or not goal:
        return None
    frontier= [start]
    visited = set()
    path = {start: [start]}
    while frontier:
        current=frontier.pop()
        if current== goal:
            return path[current]
        if current not in visited:
            visited.add(current)
            neighbor=board.get_neighbors(current)
            neighbor.sort(key= lambda x: heuristic(x,goal), reverse=True)
            for pos in neighbor:
                frontier.append(pos)
                if (pos) not in path:
                    path[pos] = path[current] + [pos]
    return None

            
    


def Asearch(board):
    '''A*search
    '''
    start = board.start_pos
    goal = board.goal_pos
    if not start or not goal:
        return None

    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current_priority, current = heapq.heappop(frontier)

        if current == goal:
            return reconstruct_path(came_from, start, goal)

        for neighbor in board.get_neighbors(current):
            new_cost = cost_so_far[current] + 1  # Assume each move has a cost of 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    return None

def DLS(board, depth_limit):
    '''Depth-Limited Search'''
    start = board.start_pos
    goal = board.goal_pos
    if not start or not goal:
        return None 
    
    if depth_limit <= 0:
        return None  # Reached depth limit without finding goal
    
    # Initialize the stack with the starting position
    stack = [(start, [start])]
    # Set to keep track of visited nodes
    visited = set()
    visited.add(start)
    
    while stack:
        current, path = stack.pop()
        
        # Get the neighbors of the current node
        neighbors = board.get_neighbors(current)
        
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                if neighbor == goal:
                    return path + [neighbor]  # Return the path to the goal
                elif len(path) < depth_limit:  # Check depth limit
                    stack.append((neighbor, path + [neighbor]))
    
    return None  # If no path found within this depth limit
