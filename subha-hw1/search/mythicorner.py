class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print 'Warning: no food in corner ' + str(corner)
        self._expanded = 0 # Number of search nodes expanded
        # Please add any code here which you would like to use
        # in initializing the problem
        "*** YOUR CODE HERE ***"
        self.Remaining = self.corners

    def getStartState(self):
        "Returns the start state (in your state space, not the full Pacman state space)"
        "*** YOUR CODE HERE ***"

        return ((self.startingPosition,self.Remaining ))

        #util.raiseNotDefined()

    def isGoalState(self, state):
        "Returns whether this search state is a goal state of the problem"
        "*** YOUR CODE HERE ***"



        if (len(state[1]) == 0):
            return True
        else:
            return False

        #util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """


        successors = []

        (x,y) = state[0]
        Remaining = []
        cornersLeft=state[1]
        for c in state[1]:
            Remaining.append(c)

        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            (dx, dy) = Actions.directionToVector(action)
            (nextx, nexty) = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]
            if (hitsWall == False):
                newCornersLeft = []
                for c in cornersLeft:
                    newCornersLeft.append(c)
                    Remaining = newCornersLeft
                if (Remaining.count((nextx,nexty)) != 0):
                    Remaining.remove((nextx,nexty))
                successors.append((((nextx, nexty), tuple(Remaining)), action, 1))

        self._expanded += 1
        return successors
