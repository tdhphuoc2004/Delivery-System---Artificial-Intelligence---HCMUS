import Visuallize
from Board import Board
from level1 import DFS, UCS, IDS, BFS, GBFS, Asearch
from level3 import A_star_search,GDFS
from level2 import Asearch2,UCS_2
if __name__ == "__main__":
    matrix,time,fuel = Visuallize.read_file("input1_level2.txt")
    board = Board(matrix, time, fuel)
    #Call search function here
    path =  UCS_2(board)
    print(path)
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