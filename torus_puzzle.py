#Author: Jeff Hank
#Date: February 9, 2020
#Class: COMP SCI 540 LEC 001
#Assignment: P2 Torus 8-Puzzle
#Files: torus_puzzle.py


''' author: hobbes
    source: cs540 canvas
'''
class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        self.max_len = 0

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def is_empty(self):
        return len(self.queue) == 0

    #adds a dictionary to the priority queue, if the state is already in the queue, it updates the existing state with
    #a new g, f, and parent
    #self - the queue of dictionaries
    #state_dict - the dictionary to be added to the queue
    def enqueue(self, state_dict):
        in_open = False
        for item in self.queue:
            if(item['state']==state_dict['state']):
                in_open = True
                if(state_dict['f'] < item['f']):
                    item['g'] = state_dict['g']
                    item['f'] = state_dict['f']
                    item['parent'] = state_dict['parent']

        if not in_open:
            self.queue.append(state_dict)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def requeue(self, from_closed):
        """ Re-queue a dictionary from the closed list (see lecture slide 21)
        """
        self.queue.append(from_closed)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def pop(self):
        """ Remove and return the dictionary with the smallest f(n)=g(n)+h(n)
        """
        minf = 0
        for i in range(1, len(self.queue)):
            if self.queue[i]['f'] < self.queue[minf]['f']:
                minf = i
        state = self.queue[minf]
        del self.queue[minf]
        return state

#takes as input two integers representing the two index of a list to be swapped
#index1 - first index
#index2 - second index
#returns a list with the values at the two indexes swapped
def swap(state,index1,index2):
    newState = state.copy()
    blank = newState[index1]
    newState[index1] = state[index2]
    newState[index2] = blank
    return newState

#finds the four possible successor states of a state
#state - parent state whose children are to be found
#returns a list of states containing the 4 successors
def succ(state):
    succList = []
    zeroLocation = state.index(0)
    # swap with tile on right
    if ((zeroLocation - 2) % 3 == 0):
        succList.append(swap(state, zeroLocation, zeroLocation - 2))
    else:
        succList.append(swap(state, zeroLocation, zeroLocation + 1))
    # swap with tile on left
    if ((zeroLocation) % 3 == 0):
        succList.append(swap(state, zeroLocation, zeroLocation + 2))
    else:
        succList.append(swap(state, zeroLocation, zeroLocation - 1))
    # swap with tile above
    if (zeroLocation == 0 or zeroLocation == 1 or zeroLocation == 2):
        succList.append(swap(state, zeroLocation, zeroLocation + 6))
    else:
        succList.append(swap(state, zeroLocation, zeroLocation - 3))
    # swap with tile below
    if (zeroLocation == 6 or zeroLocation == 7 or zeroLocation == 8):
        succList.append(swap(state, zeroLocation, zeroLocation - 6))
    else:
        succList.append(swap(state, zeroLocation, zeroLocation + 3))
    # print succ states with heuristic
    succList.sort()
    return succList

#takes in a list of states and print its contents alongside its heuristic value
#state - list of states to be printed
def print_succ(state):
    succList = succ(state)
    for item in succList:
        print(item,"h=",calcHeuristic(item),sep=" ")

#calculates the heuristic of a state by finding how many tiles are out of place
#state - state for which heuristic to be found
#returns the heuristic value
def calcHeuristic(state):
    count = 0
    for x in range(len(state)):
        if(state[x] != x+1):
            count = count + 1
    return count - 1

#solves the 8-puzzle problem given a starting state and prints the list of moves taken to reach the goal take
#state - starting state of the board
def solve(state):
    openList = PriorityQueue()
    closedList = []
    startDict = {'state': state, 'h': calcHeuristic(state), 'g': 0, 'parent': None, 'f': calcHeuristic(state)+0}
    goalState = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    gCount = 0
    goalNotFound = True
    openList.enqueue(startDict)
    while(not openList.is_empty() and goalNotFound):
        #sets currentDict to lowest cost state in the PQ
        currentDict = openList.pop()
        currentState = currentDict['state']
        #test to see whether we have found the goal state
        if(currentState==goalState):
            goalNotFound = False
            goalDict = currentDict
        else:
            closedList.append(currentDict)
            succList = succ(currentState)
        #converts successors of current state into dictionaries and adds them to PQ
        for item in succList:
            if(not any(cList['state'] == item for cList in closedList)):
                dict = {'state': item, 'h': calcHeuristic(item), 'g': currentDict['g'] + 1, 'parent': currentDict, 'f': calcHeuristic(item)+currentDict['g'] + 1}
                openList.enqueue(dict)
    printList =[]
    tempDict = goalDict
    #works backward from goalDict to find the path to the goal
    while(not tempDict['parent']==None):
        printList.append(tempDict)
        tempDict = tempDict['parent']
    printList.append(startDict)
    printList.reverse()
    for item in printList:
        print(item['state'],"  h=",item['h'], "  moves: ",item['g'],sep="")