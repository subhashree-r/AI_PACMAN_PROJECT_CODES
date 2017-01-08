# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        oldFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        g_time=0.0
        fscore=0.0
        cscore=0.0
        for i in newFood.asList():
            fscore+=1.0 /(manhattanDistance(i, newPos)*1.5)   #score is the inverse of  distance of food from pacman position
                                                              #multiplying 1.5 to the manhattan disatance is just a heuristic which helped in increasing the score
                                                              #even without multiplying , all the test cases are passed , with a lesser score.
        for ghost in newGhostStates:
          d=manhattanDistance(ghost.getPosition(), newPos)      #distance between ghost from pacman position
          if(d<=1):
            if(ghost.scaredTimer>0):
              g_time+=1000
            else:
              g_time-=100

        for capsule in currentGameState.getCapsules():  #score based on large food pellet
          d=manhattanDistance(capsule,newPos)
          if(d==0):
            cscore+=100 #if pacman captures the capsule , 100 is added
          else:
            cscore+=5/d #the inverse distance is added otherwise.

        return fscore+cscore + successorGameState.getScore()+g_time
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):


        def max_fun(gamestate, depth):

            score=[]
            ghost_state=gamestate.getNumAgents()
            if gamestate.isLose() or gamestate.isWin() or depth>self.depth :
                return self.evaluationFunction(gamestate),None
            legalactions=gamestate.getLegalActions(0)
            #v=-(float(inf))
            for a in legalactions:
                score.append(((min_fun(gamestate.generateSuccessor(0,a),1,depth)),a))

            return max(score)
        def min_fun(gamestate,ag_index,depth):
            ghostAct = gamestate.getLegalActions(ag_index)
            ghost_state=gamestate.getNumAgents()
            if gamestate.isLose() or gamestate.isWin() or depth>self.depth or not ghost_state: #check end cases
                return  self.evaluationFunction(gamestate),None
            successors=[]
            for action in gamestate.getLegalActions(ag_index):   #possible actions of the ghost
                successors.append(gamestate.generateSuccessor(ag_index, action))

            score=[]

            #updation of depth
            for succ in successors:

                if ag_index == gameState.getNumAgents() - 1: #check if pacman if so maximize
                    score.append(max_fun(succ, depth +1))  #updating the depth to depth+1
                else:
                    score.append(min_fun(succ, ag_index + 1, depth))
            return min(score)
        return max_fun(gameState,1)[1]


        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        def value(gameState, depth, alpha, beta):
            if depth == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose(): #checks if this is the last level during pacman turn/win or lose
                                                                                                            #and returns the evaluation function till then
                return (self.evaluationFunction(gameState),None)
            if depth % gameState.getNumAgents() == 0:   # num agents will be 1 if it was pacman and hence we maximize utility(remainder zero)
                return maxfun(gameState, depth, alpha, beta) #pacman
            else:
                return minfun(gameState, depth, alpha, beta) #ghost


        def minfun(gameState, depth, alpha, beta):
            actions = gameState.getLegalActions(depth % gameState.getNumAgents())# gets the legal actions of the corresponding index ghost in that depth(remainder will be 1
                                                                                    #thus referring to the ghost

            if len(actions) == 0:
                return ( self.evaluationFunction(gameState),None)  #terminal check

            temp=[]
            for action in actions:

                temp.append(value(gameState.generateSuccessor(depth % gameState.getNumAgents(), action), depth+1, alpha, beta))
                 #setting alpha and beta values
                minval=min(temp) #minimum value from temp to compare with alpha
                if minval[0] < alpha: #if minval is less than alpha , returning alpha
                    return minval
                beta = min( minval[0],beta) #beta is set as min of the minval and beta
            return minval

        def maxfun( gameState, depth, alpha, beta):
            actions = gameState.getLegalActions(0)

            if len(actions) == 0:
                return ( self.evaluationFunction(gameState),None)

            maxval = ( -99999,None) #initialising max value to -99999
            #cost=[]
            for action in actions:
                #cost.append(value(gameState.generateSuccessor(0, action), depth+1, alpha, beta))
                #maxval=max(cost)
                temp = value(gameState.generateSuccessor(0, action), depth+1, alpha, beta)
                #setting alpha and beta values
                if temp[0] > maxval[0]:
                    maxval = ( temp[0],action)

                if maxval[0] > beta:
                    return maxval
                alpha = max(alpha, maxval[0]) #setting alpha to maximum of previous alpha and maxval
            return maxval

        return value(gameState, 0, -99999, 99999)[1]#returning actions

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        def maxfun(gamestate, current_depth): # same as minmax function but the returned value is an average of the utilities


            if current_depth > self.depth or gamestate.isWin() or not gamestate.getLegalActions(0):  # checking end cases
                return self.evaluationFunction(gamestate), None

            cost = []
            for action in gamestate.getLegalActions(0): #legal actions of pacman
                successor = gamestate.generateSuccessor(0, action)
                cost.append((minfun(successor, 1, current_depth)[0], action))

            return max(cost)

        def minfun(gamestate, agent_index, current_depth):
            ghostAct = gamestate.getLegalActions(agent_index)
            if not gamestate.getLegalActions(agent_index) or gamestate.isLose(): #checking end cases
                return self.evaluationFunction(gamestate), None


            successors=[]
            for action in ghostAct: #possible actions of ghost
                successors.append(gamestate.generateSuccessor(agent_index, action))


            cost = []

            for successor in successors:
                if (agent_index == gameState.getNumAgents() - 1):
                    cost.append(maxfun(successor, current_depth + 1))
                else:
                    cost.append(minfun(successor, agent_index + 1, current_depth))
            averageScore = 0.0

            for x in cost:
                averageScore += float(x[0]) / len(cost) #taking average

            return averageScore, None

        return maxfun(gameState, 1)[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: calculate heuristics based on food, ghost and capsule.
    """
    "*** YOUR CODE HERE ***"

    pacPos = currentGameState.getPacmanPosition()
    ghostPos = currentGameState.getGhostStates()
    foodList = currentGameState.getFood()


    fscore = 0.0
    gscore = 0.0
    cscore = 0.0
    for food in foodList.asList():
        d = manhattanDistance(food, pacPos) *  manhattanDistance(food, pacPos)  #inverse food distance of food position and pacman position
        fscore += 1.0/d

    for ghost in ghostPos:
        d=manhattanDistance(ghost.getPosition(), pacPos) #inverse food distance of ghost position and pacman position
        if(d<=1):
            if(ghost.scaredTimer>0):
                gscore+=1000
            else:
                gscore-=100


    for capsule in currentGameState.getCapsules(): #score based on large pellet
          d=manhattanDistance(capsule,pacPos)
          if(d==0):
            cscore+=10
          else:
            cscore+=5/d


    return  gscore  + currentGameState.getScore() + fscore + cscore



# Abbreviation
better = betterEvaluationFunction
