import Visuallize
import random
from Board import Board
from level1 import DFS, UCS, IDS, BFS, GBFS, Asearch
from level3 import A_star_search,gbfs
from level2 import Asearch2,UCS_2
#Test 1 of gbfs is intial fuel is sufficent to reach the goal due to matthan distances
#Test 2 of gbfs is the same test 1, but the car cant reach the goal due to the obstacles, so it should find another way 
#Test 3 of gbfs is a sample case of lv3 task 
#Test 4 of gbfs is initial fuel is not sufficent to reach the goal, so it find stations but cant reach the goal 
if __name__ == "__main__":
    # matrix,time,fuel = Visuallize.read_file("input1_level2.txt")
    # board = Board(matrix, time, fuel)
    # #Call search function here
    # path =  DFS(board)
    # print(path)
    # Visuallize.write_file('output.txt',path)
    # #Visualize map 
    # #print(limit)
    # Visuallize.start(board, path) 


    matrix,time,fuel = Visuallize.read_file("input1_level2_5.txt")
    board = Board(matrix, time, fuel)
    #Call search function here
    path =  Asearch2(board)
    Visuallize.write_file('output.txt',path)
    #Visualize map 
    #print(limit)
    vehicle = random.randint(1,9)
    Visuallize.start(board, path) 