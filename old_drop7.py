import random
import copy
import sys

#1-7 are the numbered discs, 8 is a broken disc, 9 is solid
num_discs = [1,2,3,4,5,6,7]
init_discs = [1,2,3,4,5,6,7,9] #can't init a broken disc 
all_discs = [1,2,3,4,5,6,7,8,9]

class Drop7Error(AttributeError):
	"This class is used to indicate a problem in the Drop7 game."

class Drop7(object):
	"""
	This class implements Drop7
	"""
	def __init__(self, mode, usePhone=False):
		self.board = [[] for i in range(7)]
		self.mode = mode
		self.score = 0
		self.chain = 0
		self.drops = 0
		self.maxDrops = 5 if mode == "Blitz" else 30
		self.usePhone = usePhone
	
	def __str__(self):
		s = "---------------------------\n"
		for row in range(7):
			line = ""
			for col in range(7):
				if row < len(self.board[col]):
					add = "(" + str(self.board[col][row]) + ") "
				else:
					add = "( ) "
				line = line + add	
			s = line + "\n" + s
		s = "\n---------------------------\n" + s
		return s
	
	def initiateGame(self):
		if self.mode == "Blitz":
			self.initiateBlitz()
		else:
			exit("Error: Other Modes Not Supported")
	
	def initiateBlitz(self):
		if self.usePhone:
			pieces = input("The Number Of Pieces On The Board: ")
			for i in range(pieces):
				d = self.initiateDisc()
				row = input("Row: ")
				col = input("Column: ")
				self.dropDisc(d, col)
		else:
			pieces = random.randrange(8,12)
			for i in range(pieces):
				d = self.initiateDisc()
				self.dropDisc(d, random.randrange(7))

	def initiateDisc(self):
		if self.usePhone:
			v = None
			while v not in init_discs:
				v = input("""
Choose A Disc:
	1: 1
	2: 2
	3: 3
	4: 4
	5: 5
	6: 6
	7: 7
	9: Solid""")
		else:
			v = random.choice(num_discs)
		return Disc(v)
	
	def dropDisc(self, disc, col):
		self.board[col].append(disc)
	
	def crashable(self, disc, row, col):
		if disc.type == "s":
			return
	
	def stable(self):
		for col in range(len(self.board)):
			for row in range(len(self.board[col])):
				disc = self.board[col][row]
				if self.discsInRow(row) == disc.type or self.discsInCol(Col) == disc.type:
					return False
		return True

	def discInCol(col):
		return len(self.board[col])

	def discInRow(disc, row):
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
	
	def levelUp(self):
		self.board.insert(0, [9 for i in range(7)])

	def playGame(self):
		self.initiateGame()	
		if self.stable():
			return

class Disc(object):
	"""
	This class implements Drop7 discs.
	"""
	def __init__(self, typ):
		self.type = typ

	def __str__(self):
		return str(self.type)


if __name__ == "__main__":
	game = Drop7("Blitz", False)
	print(game)
