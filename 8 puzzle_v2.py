from collections import deque # for using default queue data structure
import subprocess as sp # for clear screen
import time, copy # for running time and copying arrays
opened = deque()    
closed = deque()
ancestor = deque()  
goal = [[1,2,3],
        [4,5,6],
        [7,8,0]]

start = [[1,3,6],
         [5,2,0],
         [4,7,8]]
empty = -1
layer_cost = 0
#===================================================

class Tree():
    def __init__(self,parent):
        self.parent = parent
        self.data = [[0,0,0],[0,0,0],[0,0,0]]
        self.child = []
        self.r = 0
        self.c = 0
        self.hn = 0
        self.gn = 0
        self.fn = 0

    def get_child_data(self):  # member function to generate children of a node
        self.child = [Tree(self) for i in range(4)]
        global layer_cost
        layer_cost += 1
        i, j = 0, 0
        for p in range(4):
            arr = 0
            arr = copy.deepcopy(self.data)
            if p == 0 and self.r != 0:
                i, j = -1, 0
            elif p == 1 and self.r != 2:
                i, j = 1, 0
            elif p == 2 and self.c != 0: 
                i, j = 0, -1
            elif p == 3 and self.c != 2:
                i, j = 0, 1
                
            temp = arr[self.r][self.c]
            arr[self.r][self.c] = arr[self.r+i][self.c+j]
            arr[self.r+i][self.c+j] = temp
            
            self.child[p].r = self.r+i
            self.child[p].c = self.c+j
            self.child[p].data = check(arr)
            self.child[p].gn = self.gn + layer_cost
            self.child[p].hn = get_hn(self.child[p].data)
            self.child[p].fn = self.child[p].gn + self.child[p].hn

def record_ancestor(node): # function to store the nodes from root node to current node
    ancestor.clear()
    ancestor.appendleft(node)
    while(node.parent != None):
        ancestor.appendleft(node.parent)
        node = node.parent
    
def results(): # function to diplay results after the search completes
    for nodes in ancestor: 
        display(nodes.data)
        time.sleep(.5)
        # sp.call('clear', shell=True)

def Best_first_search(): # returns node to expand next based on best first search algorithm
    temp = opened.pop()
    opened.append(temp)
    lowhn = temp.hn
    for nodes in opened:
        if nodes.hn <= lowhn:
            lowhn = nodes.hn
    for nodes in opened:
        if nodes.hn == lowhn:
            return nodes

def A_star(): # returns node to expand next based on A* search algorithm
    temp = opened.pop()
    opened.append(temp)
    lowfn = temp.fn
    for node in opened:
        if node.fn <= lowfn:
            lowfn = node.fn
    for node in opened:
        if node.fn == lowfn:
            return node

def Breadth_First_Search(): # returns node to expand next based on breadth first search algorithm
    temp = opened.pop()
    opened.appendleft(temp)
    return temp
    
def expand(algo_number): # function the expand a node
    while (len(opened) > 0):
        if algo_number == 1:
            x = A_star()
        elif algo_number == 2:
            x = Best_first_search()
        else:
            x = Breadth_First_Search()
        record_ancestor(x)
        opened.remove(x)
        closed.append(x)
        x.get_child_data()
        if x.data == goal:
            end_time = time.time()
            results()
            print('total time taken (seconds)',end_time - start_time)
            print('number of nodes expanded', len(closed))
            return 0
        for t in range(4):
            if x.child[t].data != empty:
                opened.append(x.child[t])
    else:
        print("state not found")

def display(arr): # function to display a particular state
    if arr != empty:
        for i in range(3):
            print("")
            for j in range(3):
                print(arr[i][j], end = ' ')
    print("")
    time.sleep(1)
#-----------------------------------------------
def get_hn(arr): # function to return the heuristic value of a node
    if arr != empty:
        count = 0
        for i in range(3):
            for j in range(3):
                if arr[i][j] != goal[i][j]:
                    count += 1
        return count
    else:
        return 0
#---------------------------------------------------------------------
def check(arr): # checks whether a child is valid
    for nodes in closed:
        if nodes.data == arr:
            return empty
    for nodes in opened:
        if nodes.data == arr:
            return empty
    return arr
#------------------------------------------------------------------------
if __name__ == "__main__":
    print('        START STATE        GOAL STATE ')
    print('       -------------     -------------')
    print(f'        {start[0]}          {goal[0]}')
    print(f'        {start[1]}          {goal[1]}')
    print(f'        {start[2]}          {goal[2]}')
    print('')
    print('Available algorithms to use:')
    print('1. A* (A star)')
    print('2. Best First Search')
    print('3. Breadth First Search BFS')
    not_valid = True
    while(not_valid):
        algo_number = int(input('Select option (1/2/3) :'))
        if algo_number in [1, 2, 3]:
            not_valid = False
    if algo_number == 1:
        print('USING A* SEARCH ALGORITHM..')
    elif algo_number == 2:
        print('USING BEST FIRST SEARCH ALGORITHM..')
    else:
        print('USING BREADTH FIRST SEARCH ALGORITHM..')

    start_time = time.time()
    root = Tree(None)
    root.data = start
    for i in range(3):
        for j in range(3):
            if root.data[i][j] == 0:
                root.r = i
                root.c = j
                j = 2
                i = 2
    root.gn = 0
    root.hn = get_hn(root.data)
    root.fn = root.gn + root.hn
    opened.append(root)
    expand(algo_number)