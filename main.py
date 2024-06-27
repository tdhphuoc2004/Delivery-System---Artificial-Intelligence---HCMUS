import Visuallize
from Board import Board
from level1 import DFS, UCS, IDS, BFS, GBFS


if __name__ == "__main__":
   # Visuallize.main() #co sys.exit() nen phai comment neu muon chay code duoi
    matrix = Visuallize.read_file("input1_level1.txt")
    board = Board(matrix)
    print(matrix)
    path, depth_limit = IDS(board)
    
    if path:
        print("Path found:")
        for step in path:
            print(step)
        print(f"Depth limit: {depth_limit}")
    else:
        print("Path not found within depth limits")