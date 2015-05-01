from drop7 import *
from random import random, randrange

class MinimaxNode(object):
    def __init__(self, state, move, depth, player):
        self.state = state
        self.move = move
        self.depth = depth
        self.player = player

class MinimaxPlayer(Konane, Player):
    def __init__(self, size, depthLimit, verbose=False):
        Drop7.__init__(self)           # construct the game
        self.limit = depthLimit        # cutoff level of search 
        self.verbose = verbose         # flag used to view debugging messages
        self.bestScore = 1000000       # best possible score for maximizer
        self.worstScore = -1000000     # worst possible score for maximizer

    def initialize(self, side):
        self.name = "MinimaxPlayerDepth" + str(self.limit)
        self.side = side

    def getMove(self, board):
        root = MinimaxNode(board, None, 0, self.side)
        return self.boundedMinimax(root)

    def eval(self, node):
        '''
        This static evaluator uses the number of unique moves a
        player has, and the number of border pieces the player has. I
        chose those two features because counting the unique moves is
        better than counting all the moves a player has, since
        sometimes one piece could have multiple possible moves, but
        could excute one. Also, the border pieces increase the score
        for a player because a player's border pieces can eat other
        pieces but can't be eaten.
        '''
        blackMoves = self.generateMoves(node.state, 'B')
        if len(blackMoves) == 0: return self.worstScore
        whiteMoves = self.generateMoves(node.state, 'W')
        if len(whiteMoves) == 0: return self.bestScore
        blackSet = set([tuple(move[:2]) for move in blackMoves])
        whiteSet = set([tuple(move[:2]) for move in whiteMoves])
        blackBorder = [x for x in blackSet if 0 in x or self.size-1 in x] 
        whiteBorder = [x for x in whiteSet if 0 in x or self.size-1 in x]
        return len(blackSet) + len(blackBorder) - len(whiteSet) - len(whiteBorder)

    def boundedMinimax(self, node):
        if self.verbose: print " " * node.depth + "BEGIN boundedMiniMax"
        values = []
        moves = self.generateMoves(node.state, node.player)
        if len(moves) == 0: return None
        for move in moves:
            nextState = self.nextBoard(node.state, node.player, move)
            nextNode = MinimaxNode(nextState, move, node.depth+1, self.opponent(node.player))
            values.append(self.minValue(nextNode))
        maxIndex = values.index(max(values))
        if self.verbose:
            print " " * node.depth + "Moves: %s"%(moves)
            print " " * node.depth + "Values: %s"%(values)
            print " " * node.depth + "Best move: %s with value %s"%(moves[maxIndex], values[maxIndex])
            print " " * node.depth + "END boundedMinimax"
        return moves[maxIndex]

    def minValue(self, node):
        #return (random() * 6) - 3
        if self.verbose: print " " * node.depth + "BEGIN minValue"
        if node.depth == self.limit:
            if self.verbose: print " " * node.depth + "END minValue at depth limit returning", self.eval(node)
            return self.eval(node)
        moves = self.generateMoves(node.state, node.player)
        if len(moves) == 0: 
            if self.verbose: print " " * node.depth + "End minValue no moves returning", self.eval(node)
            return self.eval(node)
        v = self.bestScore
        for move in moves:
            nextState = self.nextBoard(node.state, node.player, move)
            nextNode = MinimaxNode(nextState, move, node.depth+1, self.opponent(node.player))
            v = min(v, self.maxValue(nextNode))
        if self.verbose:
            print " " * node.depth + "END minValue, returning %d"%(v)
        return v

    def maxValue(self, node):
        #return (random() * 6) - 3
        if self.verbose: print " " * node.depth + "BEGIN maxValue"
        if node.depth == self.limit:
            if self.verbose: print " " * node.depth + "END maxValue at depth limit returning", self.eval(node)
            return self.eval(node)
        moves = self.generateMoves(node.state, node.player)
        if len(moves) == 0: 
            if self.verbose: print " " * node.depth + "End maxValue no moves returning", self.eval(node)
            return self.eval(node)
        v = self.worstScore
        for move in moves:
            nextState = self.nextBoard(node.state, node.player, move)
            nextNode = MinimaxNode(nextState, move, node.depth+1, self.opponent(node.player))
            v = max(v, self.minValue(nextNode))
        if self.verbose:
            print " " * node.depth + "END maxValue, returning %d"%(v)
        return v

if __name__ == '__main__':    
    game = Konane(6)
    wins = 0
    losses = 0
    for i in range(100):
        #print i
        result = game.playOneGame(MinimaxPlayer(6, 4), RandomPlayer(6), False)
        if result == 'B':
            print "Black wins"
            wins+=1
        else:
            print "White wins"
            losses+=1
    print "Wins", wins, "Losses", losses

    #game = Konane(6)
    #game.playOneGame(MinimaxPlayer(6, 4, False), RandomPlayer(6))

    #game = Konane(6)
    #game.playOneGame(MinimaxPlayer(6, 2, True), SimplePlayer(6))

