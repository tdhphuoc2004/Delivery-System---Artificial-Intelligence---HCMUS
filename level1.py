import heapq

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

def DFS(board):
    '''Depth-First-Search
    '''

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

def GBFS(board):
    '''Greedy Best First Search
    '''

def Asearch(board):
    '''A*search
    '''

