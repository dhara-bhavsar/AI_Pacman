# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
#         return successorGameState.getScore()
        score = successorGameState.getScore()

        foodList = newFood.asList()
        closestFoodDist = 100
        for food in foodList:
            dist = util.manhattanDistance(food, newPos)
            if dist < closestFoodDist:
                closestFoodDist = dist
        if currentGameState.getNumFood() > successorGameState.getNumFood():
            score += 100
        if action == Directions.STOP:
            score -= 3
        score -= 3 * closestFoodDist

        capsulePos = currentGameState.getCapsules()
        if successorGameState.getPacmanPosition() in capsulePos:
            score += 120

        for ghostIndex in range(currentGameState.getNumAgents()):
            if ghostIndex != 0:
                ghostPos = currentGameState.getGhostPosition(ghostIndex)
                distFromGhost = util.manhattanDistance(ghostPos, newPos)
                score += max(distFromGhost, 3)
                # if newScaredTimes == 0 and distFromGhost == 1:
                #     score -= 30

        return score

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
#         util.raiseNotDefined()
        
        # Assigning Pacman Index to a constant
        pIndex = 0

        def maxAgent(state, nodeLevel):
            if state.isLose() or state.isWin():
                return state.getScore()
            # highest score for a Max Agent is negative infinity
            highestScore = float("-inf")
            actions = state.getLegalActions(pIndex)
            score = highestScore
            optimalAction = Directions.EAST
            for action in actions:
                if action != Directions.STOP:
                    score = minAgent(state.generateSuccessor(pIndex, action), nodeLevel, 1)
                    if score > highestScore:
                        highestScore = score
                        optimalAction = action
            if nodeLevel == 0:
                return optimalAction
            else:
                return highestScore

        def minAgent(state, nodeLevel, ghost):
            if state.isLose() or state.isWin():
                return state.getScore()
            # highest score for a Min Agent is positive infinity
            highestScore = float("inf")
            nextAgent = ghost + 1
            if ghost == state.getNumAgents() - 1:
                nextAgent = pIndex
            actions = state.getLegalActions(ghost)
            score = highestScore
            for action in actions:
                if action != Directions.STOP:
                    if nextAgent == pIndex:
                        if nodeLevel == self.depth - 1:
                            score = self.evaluationFunction(state.generateSuccessor(ghost, action))
                        else:
                            score = maxAgent(state.generateSuccessor(ghost, action), nodeLevel + 1)
                    else:
                        score = minAgent(state.generateSuccessor(ghost, action), nodeLevel, nextAgent)
                    if score < highestScore:
                        highestScore = score
            return highestScore

        return maxAgent(gameState, 0)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
#         util.raiseNotDefined()
        
        pIndex = 0 # Assigning Pacman Index to a constant

        def maxAgent(state, nodeLevel, alpha, beta):
            if state.isLose() or state.isWin():
                return state.getScore()
            # highest score for a Max Agent is negative infinity
            highestScore = float("-inf")
            actions = state.getLegalActions(pIndex)
            score = highestScore
            optimalAction = Directions.EAST
            for action in actions:
                if action != Directions.STOP:
                    score = minAgent(state.generateSuccessor(pIndex, action), nodeLevel, 1, alpha, beta)
                    if score > highestScore:
                        highestScore = score
                        optimalAction = action
                    alpha = max(alpha, highestScore)
                    if highestScore > beta:
                        return highestScore
            if nodeLevel == 0:
                return optimalAction
            else:
                return highestScore

        def minAgent(state, nodeLevel, ghost, alpha, beta):
            if state.isLose() or state.isWin():
                return state.getScore()
            # highest score for a Min Agent is positive infinity
            highestScore = float("inf")
            nextAgent = ghost + 1
            if ghost == state.getNumAgents() - 1:
                nextAgent = pIndex
            actions = state.getLegalActions(ghost)
            score = highestScore
            for action in actions:
                if action != Directions.STOP:
                    if nextAgent == pIndex:
                        if nodeLevel == self.depth - 1:
                            score = self.evaluationFunction(state.generateSuccessor(ghost, action))
                        else:
                            score = maxAgent(state.generateSuccessor(ghost, action), nodeLevel + 1, alpha, beta)
                    else:
                        score = minAgent(state.generateSuccessor(ghost, action), nodeLevel, nextAgent, alpha, beta)
                    if score < highestScore:
                        highestScore = score
                    beta = min(beta, highestScore)
                    if highestScore < alpha:
                        return highestScore
            return highestScore

        return maxAgent(gameState, 0, float("-inf"), float("inf"))

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
#         util.raiseNotDefined()
        
#         pIndex = 0 # Assigning Index to Pacman
# 
#         def maxAgent(state, nodeLevel):
#             if state.isLose() or state.isWin():
#                 return self.evaluationFunction(state)
#             # highest score for a Max Agent is negative infinity
#             highestScore = float("-inf")
#             actions = state.getLegalActions(pIndex)
#             score = highestScore
#             optimalAction = Directions.EAST
#             for action in actions:
#                 score = minAgent(state.generateSuccessor(pIndex, action), nodeLevel, 1)
#                 if score > highestScore:
#                     highestScore = score
#                     optimalAction = action
#             if nodeLevel == 0:
#                 return optimalAction
#             else:
#                 return highestScore
# 
#         def minAgent(state, nodeLevel, ghost):
#             if state.isLose() or state.isWin():
#                 return self.evaluationFunction(state)
#             # highest score for a Min Agent is positive infinity
#             highestScore = float("inf")
#             nextAgent = ghost + 1
#             if ghost == state.getNumAgents() - 1:
#                 nextAgent = pIndex
#             actions = state.getLegalActions(ghost)
#             score = highestScore
#             for action in actions:
#                 chance = 1.0/len(actions)
#                 if nextAgent == pIndex:
#                     if nodeLevel == self.depth - 1:
#                         # score = chance * self.evaluationFunction(state.generateSuccessor(ghost, action))
#                         score = self.evaluationFunction(state.generateSuccessor(ghost, action))
#                         score += chance * score
#                     else:
#                         # score = chance * maxAgent(state.generateSuccessor(ghost, action), nodeLevel + 1)
#                         score = maxAgent(state.generateSuccessor(ghost, action), nodeLevel + 1)
#                         score += chance * score
#                 else:
#                     # score = chance * minAgent(state.generateSuccessor(ghost, action), nodeLevel, nextAgent)
#                     score = minAgent(state.generateSuccessor(ghost, action), nodeLevel, nextAgent)
#                     score += chance * score
#             return score
# 
#         return maxAgent(gameState, 0)

# Solving Expectimax using other way rathan than reusing the Minimax algorithm for taking out average of the min agents

        def expectedAgent(gameState, agentindex, nodeLength):
            if gameState.isWin() or gameState.isLose() or nodeLength == 0:
                return self.evaluationFunction(gameState)
            noOfAgents = gameState.getNumAgents() - 1
            actions = gameState.getLegalActions(agentindex)
            numactions = len(actions)
            totalvalue = 0
            for action in actions:
                nextState = gameState.generateSuccessor(agentindex, action)
                if (agentindex == noOfAgents):
                    totalvalue += maxAgent(nextState, nodeLength - 1)
                else:
                    totalvalue += expectedAgent(nextState, agentindex + 1, nodeLength)
            return totalvalue / numactions

        def maxAgent(gameState, nodeLength):
            if gameState.isWin() or gameState.isLose() or nodeLength == 0:
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(0)
            optimalAction = Directions.STOP
            score = float("-inf")
            for action in actions:
                oldScore = score
                nextState = gameState.generateSuccessor(0, action)
                score = max(score, expectedAgent(nextState, 1, nodeLength))
            return score


        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(0)
        optimalAction = Directions.STOP
        score = float("-inf")
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            oldScore = score
            score = max(score, expectedAgent(nextState, 1, self.depth))
            if score > oldScore:
                optimalAction = action
        return optimalAction



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      
      Here I have firstly I have taken the currentGameState score and on it I have checked the nearest possible 
      food around PacMan and have wanted him to go for it keeping in-check the nearby ghost agents. But it in turn
      did not go for the isolated food. So have given incentive to PacMan by subtracting 4.5 for each remaining food 
      number such that it would prefering eating farther food as well.
      Then on eating ghosts more points are scored hence whenever near the capsule the PacMan would be eager to eat it 
      if some ghost is in vicinity.
      Lastly the most important thing was keeping the PacMan away from the ghosts.
      Also I have made sure that winning is the primary goal of the PacMan by assigning infinity points on winning and vice
      versa for the losing game.
      
    """
    "*** YOUR CODE HERE ***"
#     util.raiseNotDefined()

    pIndex = 0

    finalScore = scoreEvaluationFunction(currentGameState)
    foods = currentGameState.getFood()
    foodPos = foods.asList()
    nearestfood = float("inf")
    for food in foodPos:
        tmpdist = util.manhattanDistance(food, currentGameState.getPacmanPosition())
        if (tmpdist < nearestfood):
            nearestfood = tmpdist
    finalScore -= nearestfood * 1.25
    finalScore -= 4.5 * len(foodPos)
    capsulePos = currentGameState.getCapsules()
    finalScore -= 3 * len(capsulePos)
    distToGhost = float("inf")
    for agentIndex in range(currentGameState.getNumAgents()):
        if agentIndex != pIndex:
            nextdist = util.manhattanDistance(currentGameState.getPacmanPosition(), currentGameState.getGhostPosition(agentIndex))
            distToGhost = min(distToGhost, nextdist)
    finalScore += max(distToGhost, 3.5) * 2.25
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")

    return finalScore

# Abbreviation
better = betterEvaluationFunction

