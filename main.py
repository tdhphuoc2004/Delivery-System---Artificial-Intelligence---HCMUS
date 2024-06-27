import Visuallize
from Board import Board
from level1 import UCS
from level1 import BFS
from level1 import GBFS

if __name__ == "__main__":
    #Visuallize.main() #co sys.exit() nen phai comment neu muon chay code duoi
    matrix = Visuallize.read_file("input1_level1.txt")
    board = Board(matrix)
    print(matrix)
    path = GBFS(board)
    if path:
        for step in path:
            print(step)
    else:
        print("not found")
