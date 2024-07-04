import heapq
from level1 import reconstruct_path
from level1 import heuristic

def Asearch2(board, time):
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
            if cost_so_far[current]<=time:
                return reconstruct_path(came_from, start, goal)
            else:
                return None

        for neighbor in board.get_neighbors(current):
            x, y=current
            new_cost = cost_so_far[current] + board.get_cost(x,y)  
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    return None