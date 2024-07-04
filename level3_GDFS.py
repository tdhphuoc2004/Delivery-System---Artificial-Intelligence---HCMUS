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