# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from game import Directions

    frontier=util.Stack() # we use stack
    start=problem.getStartState()
    curstate=start
    #frontier.push(None,problem.getStartState(),'Finish')
    action=[]
    frontier.push((start,[],0))
    visited=[]
    path=[]

    while (not frontier.isEmpty()):
        cur_temp=frontier.pop()
        cur_temp_state=cur_temp[0]
        if (problem.isGoalState(cur_temp_state)):
            path=cur_temp[1]
            break
        if (cur_temp_state not in visited):
            visited.append(cur_temp_state)
            successors= problem.getSuccessors(cur_temp_state)
            for i in successors:
                if i[0] not in visited:
                    frontier.push((i[0],cur_temp[1]+[i[1]],cur_temp[2]+i[2]))


    #successors= problem.getSuccessors()
    return path


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    frontier=util.Queue()# we use a queue as we want the primary nodes at each level to be tested before expanding children.
                        #Since queue return the old (last in first out node every time , this ensures the nodes at each level is expanded before moving to next node.
    start=problem.getStartState()
    curstate=start
    #frontier.push(None,problem.getStartState(),'Finish')
    action=[]
    frontier.push((start,[],0)) #We define a priority queue
    visited=[]
    path=[]

    while (not frontier.isEmpty()):
        cur_temp=frontier.pop()
        cur_temp_state=cur_temp[0]
        if (problem.isGoalState(cur_temp_state)):
            path=cur_temp[1]
            break
        if (cur_temp_state not in visited):
            visited.append(cur_temp_state)
            successors= problem.getSuccessors(cur_temp_state)
            for i in successors:
                if i[0] not in visited:
                    frontier.push((i[0],cur_temp[1]+[i[1]],cur_temp[2]+i[2]))
    #util.raiseNotDefined()
    return path
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier=util.PriorityQueue()
    start=problem.getStartState()
    curstate=start
    #frontier.push(None,problem.getStartState(),'Finish')
    action=[]
    frontier.push((start,[],0),0)# we push the state along with the cost and follow the same tecnique as BFS
    visited=[]
    path=[]

    while (not frontier.isEmpty()):
        cur_temp=frontier.pop()
        cur_temp_state=cur_temp[0]
        if (problem.isGoalState(cur_temp_state)):
            path=cur_temp[1]
            break
        if (cur_temp_state not in visited):
            visited.append(cur_temp_state)
            successors= problem.getSuccessors(cur_temp_state)
            for i in successors:
                if i[0] not in visited:
                    frontier.push((i[0],(cur_temp[1]+[i[1]]),(cur_temp[2]+i[2])),(cur_temp[2]+i[2]))
    #util.raiseNotDefined()
    return path
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    #"*** YOUR CODE HERE ***"
     # "*** YOUR CODE HERE ***"
    frontier=util.PriorityQueue()
    start=problem.getStartState()
    curstate=start
    #frontier.push(None,problem.getStartState(),'Finish')
    action=[]
    heur=heuristic(start,problem)
    frontier.push((start,[],0),(0+heur))
    visited=[]
    path=[]

    while (not frontier.isEmpty()):
        cur_temp=frontier.pop()
        cur_temp_state=cur_temp[0]
        if (problem.isGoalState(cur_temp_state)):  #checks if it's goal state ,and is it is then it returns the path else stores the action of the current state
            path=cur_temp[1]
            break
        if (cur_temp_state not in visited):
            visited.append(cur_temp_state)
            successors= problem.getSuccessors(cur_temp_state)
            for i in successors:
                if i[0] not in visited:
                    heur=heuristic(i[0],problem)
                    frontier.push((i[0],(cur_temp[1]+[i[1]]),(cur_temp[2]+i[2])),(cur_temp[2]+i[2]+heur))# adds the current action, heuristic, money with previos and returns
    #util.raiseNotDefined()
    return path
    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
