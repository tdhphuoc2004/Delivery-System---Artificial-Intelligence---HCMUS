import Visuallize
from Board import Board
from level1 import DFS, UCS, IDS, BFS, GBFS


if __name__ == "__main__":
    matrix = Visuallize.read_file("input1_level1.txt")
    board = Board(matrix)
    #Call search function here
    path, depth_limit = IDS(board)
    #Visualize map 
    Visuallize.start(board, path) 

    #Some information about search
    # if path:
    #     print("Path found:")
    #     for step in path:
    #         print(step)
    #     print(f"Depth limit: {depth_limit}")
    # else:
    #     print("Path not found within depth limits")