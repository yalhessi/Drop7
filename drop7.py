import random
import copy
import sys
import os
import argparse

#1-7 are the numbered discs, 8 is a broken disc, 9 is solid
num_discs = [1,2,3,4,5,6,7]
init_discs = [1,2,3,4,5,6,7,9] #can't init a broken disc 
all_discs = [1,2,3,4,5,6,7,8,9]
chain_factor = [7, 39, 109, 224, 391, 617, 907, 1267, 1701, 2213, 2809, 3491, 4265, 5133, 6099, 7168, 8341, 9622, 11014, 12521, 14146, 15891, 17758, 19752, 21875, 24128, 26515, 29039, 31702, 34506]

class Drop7Error(Exception):
	"This class is used to indicate a problem in the Drop7 game."
	def __str__(self):
		return repr("Error: " + self.args[0])


class Drop7(object):
	"""
	This class implements Drop7
	"""
	def __init__(self, verbose=False):
		if verbose: print "Begin Drop7 __init__"
		self.board = [[] for i in range(7)]
		self.score = 0
		self.level = 0
		self.chain = 0
		self.drops = 0
		self.maxDrops = 5
		self.dropping = Disc(None)
		self.verbose = verbose
		if verbose: print "End Drop7 __init__"

	def __str__(self):
		if not self.verbose: os.system("clear")
		s = '---------------------------\n 1   2   3   4   5   6   7\n'
		for row in range(7):
			line = ""
			for col in range(7):
				if row < len(self.board[col]):
					#add = "(" + str(self.board[col][row]) + ") "
					line += str(self.board[col][row])
				else:
					line += "( ) "
				#line = line + add	
			s = line + "\n" + s
		s = "Drop7 Game\n\nLevel: %d\nDrops Left: %d\n\nCurrent Score: %d\n            %s\n---------------------------\n" % (self.level, (5-(self.drops%self.maxDrops)), self.score, self.dropping) + s
		return s
	
	def initiateDisc(self):
		if self.verbose: print "Inside Drop7 initiateDisc"
		return Disc(random.choice(init_discs))

	def initiateNumDisc(self):
		if self.verbose: print "Inside Drop7 initiateNumDisc"
		return Disc(random.choice(num_discs))

	def breakDisc(self, d):
		if self.verbose: print "Inside Drop7 breakDisc"
		if d.type == 9:
			d.type = 8
		elif d.type == 8:
			d.type = random.choice(num_discs)
		elif 0 < d.type < 8:
			return
		else:
			raise Drop7Error("Invalid Input %d", d)
	
	def dropDisc(self, disc, col):
		if self.verbose: print "Inside Drop7 dropDisc"
		self.board[col].append(disc)

	def dropNewDisc(self):
		if self.verbose: print "Inside Drop7 dropNewDisc"
		self.dropping = self.initiateNumDisc()
		print(self)
		col = None
		while (col not in frozenset(range(7))) or (col is not None and len(self.board[col]) >= len(self.board)):
			col = input("Drop Current Disc At Column: ") - 1
		self.dropDisc(self.dropping, col)
		self.drops += 1
		self.chain = 0

	def initiateGame(self):
		if self.verbose: print "Inside Drop7 initiateGame"
		pieces = random.randrange(12,16)
		for i in range(pieces):
			d = self.initiateNumDisc()
			self.dropDisc(d, random.randrange(7))
	
	def lenCol(self, col):
		if self.verbose: print "Inside Drop7 lenCol"
		return len(self.board[col])

	def lenRow(self, row, d):
		if self.verbose: print "Inside Drop7 lenRow"
		lst = [self.board[col][row] if row < len(self.board[col]) else None for col in range(len(self.board))]
		found = False
		start, end = 0, len(lst)
		for curr in range(len(lst)):
			if found and lst[curr] is None:
				end = curr
				break
			elif not found and lst[curr] is None:
				start = curr+1
			elif lst[curr] is d:
				found = True
		return end-start

		'''
		for j in range(len(self.board[0])):
			currRow = [self.board[i][j] for i in range(len(self.board))]
			if d in row:


		lst = []
		found = False
		for i in range(7):
			curr = self.board[i][row:row+1]
			if curr is not None:
				lst.append(curr)
				if curr == disc: found = True
			else:
				lst = []
		return lst if found else []
		'''
	def removeDisc(self, board, col, d):
		if self.verbose: print "Inside Drop7 crashDisc"
		self.score += chain_factor[self.chain]
		board[col].remove(d)

	def cleanBoard(self):
		if self.verbose: print "Inside Drop7 cleanBoard"
		if not self.isDone():
			copy = [[d for d in col] for col in self.board]
			for col in range(len(self.board)):
				for row in range(len(self.board[col])):
					disc = self.board[col][row]
					if self.lenRow(row, disc) == disc.type or self.lenCol(col) == disc.type:
						self.removeDisc(copy, col, disc)
						if col > 0 and len(self.board[col-1]) > row:
							#print ("break left") 
							self.breakDisc(self.board[col-1][row]) #left disc
						if row > 0:
							#print ("break down") 
							self.breakDisc(self.board[col][row-1]) #down disc
						if col < len(self.board)-1 and len(self.board[col+1]) > row:
							#print ("break right")
							self.breakDisc(self.board[col+1][row]) #right disc
						if row < len(self.board[col])-1:
							#print ("break up")
							self.breakDisc(self.board[col][row+1]) #up disc
			if self.board != copy:
				self.board = copy
				self.chain += 1
				if copy == [[] for i in range(7)]: score += 70000
				self.cleanBoard()
	
	def levelUp(self):
		if self.verbose: print "Inside Drop7 levelUp"
		self.level += 1
		self.score += 17000
		for col in self.board:
			col.insert(0, Disc(9))

	def isDone(self):
		for col in self.board:
			#print len(col)
			if len(col) > 7:
				return True
		for col in self.board:
			if len(col) < 7:
				return False
		return True

	def playGame(self):
		if self.verbose: print "Inside Drop7 playGame"
		self.cleanBoard()
		self.score = 0
		self.level = 1
		while not self.isDone():
			self.dropNewDisc()
			self.cleanBoard()
			if self.drops%self.maxDrops == 0:
				self.levelUp()
				self.cleanBoard()
		print "\nGame Over!\n\nFinal Score: %d" % self.score

class Disc(object):
	"""
	This class implements Drop7 discs.
	"""
	def __init__(self, typ):
		self.type = typ

	def __str__(self):
		if self.type == 9:
			return "(O) "
		elif self.type == 8:
			return "(0) "
		else:
			return "(" + str(self.type) + ") "


if __name__ == "__main__":
	#setting up the program command line
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
	args = parser.parse_args()
	if args.verbose:
		print "\nVerbosity Turned On..."

	#initializing the game
	game = Drop7(args.verbose)
	game.initiateGame()
	game.playGame()
	#print(game)
	#for i in range(5):
	#	game.dropNewDisc()
