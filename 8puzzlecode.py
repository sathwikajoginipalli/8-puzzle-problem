import copy
import math as m

class puzzleNode:
    ## puzzleNode is a class whose objects are intended to work as states from start --> goal

    goal = []
    
    def __init__(self, data, f_score, g_score, empty_loc, goal_data=None, by='start', parent_node=None):
        ## data       -> the 3x3 matrix data
        ## f_score    -> f score for the matrix (calculated by invoking calculate_f_score function)
        ## g_score    -> g score for the matrix (starts with 0 and gets incremented for each expansion)
        ## empty_loc  -> the [x,y] location of empty space
        ## goal_data  -> the 3x3 goal state data (set only while initializing the start state, default = None)
        ## by         -> operation performed on parent state so that we get current state
        ## parent_node-> parent state on which the 'by' operation is made to get current state (useful
        ##               while printing the solution from start --> goal)


        self.data = data
        self.f_score = f_score
        self.g_score = g_score
        self.by = by
        self.empty_loc = empty_loc
        self.parent_node = parent_node
        if goal_data is not None:
            puzzleNode.goal = goal_data

    def getChildren(self, method_name):
        ## Generate children from all possible moves
        children = []


        #get current location of empty space
        empty_x, empty_y = self.empty_loc

        directions = {  'left' : [empty_x, empty_y-1], 
                        'right': [empty_x, empty_y+1], 
                        'up'   : [empty_x-1, empty_y], 
                        'down' : [empty_x+1, empty_y] 
                        }
        for direction in directions.keys():
            
            if all(c in range(0,3) for c in directions[direction]):
                move_x, move_y = directions[direction]
                
                # create a new childNode from parentNode
                childNode = copy.deepcopy(self)
                
                # move empty space to desired location [move_x, move_y]
                childNode.data[empty_x][empty_y] = childNode.data[move_x][move_y]
                childNode.data[move_x][move_y] = '_'
                
                # update location of empty space
                childNode.empty_loc = [move_x, move_y]
                
                # set the operation by which current state is obtained 
                childNode.by = direction
                
                # increment g_score
                childNode.g_score += 1
                
                #calculate f_score
                childNode.calculate_f_score(method=method_name)
                
                #set parent node
                childNode.parent_node = self
                
                #add to the children list
                children.append(childNode)
        
        return children
    
    def calculate_f_score(self, method="misplaced_tiles"):
        ## To calculate the f_score of the node
        ## f_score = g_score + h_score
        h_score = 0
        if method == 'misplaced_tiles':
            #calculating h_score by the number of misplaced tiles method
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.data[i][j] != '_' and self.data[i][j] != puzzleNode.goal[i][j]:
                        h_score += 1
        if method == "manhattan":
            arr = []
            for i in range (0,3):
                for j in range (0,3):
                    arr.append(puzzleNode.goal[i][j])
                            
            for i in range (0,3):
                for j in range (0,3):
                    num = self.data[i][j]
                    i_current = i
                    j_current = j
                    index = arr.index(num)
                    i_goal, j_goal = index//3,index%3
                    if num != '_':
                        h_score += (m.fabs(i_goal - i_current) + m.fabs(j_goal - j_current))
        
        self.f_score = self.g_score + h_score

    def __eq__(self, other_node):
        ## overloading '==' operator using magic function __eq__

        if(type(other_node) is puzzleNode):
            for i in range(0,3):
                for j in range(0,3):
                    if self.data[i][j] != other_node.data[i][j]:
                        return False
        else:
            for i in range(0,3):
                for j in range(0,3):
                    if self.data[i][j] != other_node[i][j]:
                        return False
        return True
    
    def __str__(self):
        ## magic function to get custom formatted string to print puzzleNode

        return "{} \n{} \n{}\n".format(self.data[0], self.data[1], self.data[2])

class puzzleSolver:
    ## puzzleSolver is a class whose objects are intended to solve the 8-puzzle problem
    ## using puzzleNode objects as states

    no_of_nodes_generated = 0
    no_of_nodes_expanded = 0
    
    def __init__(self, initial_state, goal_state, method = "misplaced_tiles"):
        puzzleSolver.no_of_nodes_expanded = 0
        puzzleSolver.no_of_nodes_generated = 0
        self.method = method
        for i in range(0,3):
            for j in range(0,3):
                if initial_state[i][j] == '_':
                    empty_x,empty_y = i,j
        self.initial = puzzleNode(initial_state, 0, 0, [empty_x,empty_y], goal_data=goal_state)

    def solve(self):
        if self.initial == puzzleNode.goal:
            self.printAnswer(self.initial)
            return
        else:
            explored = []
            to_explore = []
            to_explore.append(self.initial)
            while len(to_explore) > 0 :
                current_node = to_explore.pop(0)
                children = current_node.getChildren(self.method)
                puzzleSolver.no_of_nodes_expanded += 1
                puzzleSolver.no_of_nodes_generated += len(children)
                explored.append(current_node)
                for child in children:
                    if child == puzzleNode.goal:
                        self.printAnswer(child)
                        return
                    else:
                        if child not in explored:
                            to_explore.append(child)
                to_explore.sort(key = lambda node : node.f_score)

    def printAnswer(self, node):
        reverse_moves = []
        moves = []
        reverse_states = []
        states = []
        path_cost = node.g_score
        while node is not None:
            reverse_moves.append(node.by)
            reverse_states.append(node)
            node = node.parent_node
        for i in range(0, len(reverse_moves)):
            moves.append(reverse_moves[-i-1])
        for i in range(0, len(reverse_states)):
            states.append(reverse_states[-i-1])
        print("-----------------------------")
        print("Method: {}".format(self.method))
        print("------------------------------")
        print("\nPath to reach the goal")
        print("==========================")
        print("-->".join(moves))
        print("==========================")
        print("Total path cost: {}".format(path_cost))
        print("Nodes generated: {}".format(puzzleSolver.no_of_nodes_generated))
        print("Nodes expanded:  {}".format(puzzleSolver.no_of_nodes_expanded))
        for state in states:
            print(" |\n\|/\n V\n")
            print(state)



start_data = input("Enter the start state: ")
goal_data = input("Enter the goal state : ")

start_data = start_data.split(' ')
goal_data = goal_data.split(' ')

start_state = [start_data[0:3], start_data[3:6], start_data[6:9]]
goal_state = [goal_data[0:3], goal_data[3:6], goal_data[6:9]]

solver = puzzleSolver(start_state, goal_state)
solver.solve()
solver = puzzleSolver(start_state, goal_state, method="manhattan")
solver.solve()
