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
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #states = mdp.getStates()
        #values = {state: 0 for state in states}
        for i in range(iterations):
            previous = self.values.copy()
            for state in mdp.getStates():
                possibleActions = mdp.getPossibleActions(state)
                if len(possibleActions) == 0: continue
                results = []
                for action in possibleActions:
                    total = 0
                    for (nextState, prob) in mdp.getTransitionStatesAndProbs(state,action):
                        total += (prob * previous[nextState])
                    results.append(total)
                self.values[state] = mdp.getReward(state) + (discount * max(results))

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def getPolicy(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        possibleActions = self.mdp.getPossibleActions(state)
        if len(possibleActions) == 0: return None
        results = []
        for action in possibleActions:
            total = 0
            for (nextState, prob) in self.mdp.getTransitionStatesAndProbs(state,action):
                total += (prob * self.values[nextState])
            results.append(total)
        maxIndex = max(enumerate(results), key=lambda x: x[1])[0]
        #print("here")
        return possibleActions[maxIndex]




    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.getPolicy(state)

