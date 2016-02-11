# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** VALUE ITERATION CODE STARTS HERE ***"
        initial_v = util.Counter()
        for itr in xrange(self.iterations):
            initial_v = self.values.copy()
            for each_state in self.mdp.getStates():
                actions = self.mdp.getPossibleActions(each_state)
                transition_functions = []
                result_values = []
                if self.mdp.isTerminal(each_state):
                    self.values[each_state] = 0
                else:
                    for each_action in actions:
                        transition_functions = self.mdp.getTransitionStatesAndProbs(each_state, each_action)
                        result_value = 0
                        for each_transition in transition_functions:
                            reward_function = self.mdp.getReward(each_state, each_action, each_transition[0])
                            result_value += (each_transition[1]
                                             * (reward_function
                                                + (self.discount
                                                   * initial_v[each_transition[0]])))
                        #     Not able to use the below function as it requires initial_v to be passed as well
                        #     as initial_v depends on iterations and keeps on changing for each iteration
                        # result_value = ValueIterationAgent.computeQValueFromValues(each_state, each_action)
                        result_values.append(result_value)
                    self.values[each_state] = max(result_values)


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** Q-VALUE FROM VALUES CODE STARTS HERE ***"
        # util.raiseNotDefined()
        transition_functions = self.mdp.getTransitionStatesAndProbs(state, action)
        result_value = 0
        for each_transition in transition_functions:
            reward_function = self.mdp.getReward(state, action, each_transition[0])
            result_value += (each_transition[1]
                             * (reward_function
                                + (self.discount
                                   * self.values[each_transition[0]])))
        return result_value


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** ACTION FROM VALUES CODE STARTS HERE ***"
        # util.raiseNotDefined()
        if self.mdp.isTerminal(state):
            return None
        else:
            best_value = float("-inf")
            best_action = 0
            actions = self.mdp.getPossibleActions(state)
            for each_action in actions:
                transition_functions = self.mdp.getTransitionStatesAndProbs(state, each_action)
                result_value = 0
                for each_transition in transition_functions:
                    result_value += (each_transition[1]
                                     * (self.mdp.getReward(state, each_action, each_transition[0])
                                        + (self.discount
                                           * self.values[each_transition[0]])))
                if result_value > best_value:
                    best_action = each_action
                    best_value = result_value
            return best_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
