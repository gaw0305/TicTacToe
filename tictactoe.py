'''
tictactoe.py

A program that implements a 4x4x4 tic-tac-toe game with AI.

Authors: Grace Whitmore and Alby Himelick
	
CS 111, Winter 2011
date: 14 March 2011
'''

from cTurtle import *
from random import *
from math import sqrt
from copy import deepcopy

'''
The definition for a Board data type.  

The Board class draws itself (first vertical, then horizontal lines, then adds roman numerals to itself); sets the window size and the width of the turtle; sets up the board matrix, which allows the computer to know where the player moved; creates dictionaries for the rows and the columns and the roman numerals of the grids in order to be able to convert player input to coordinates for a turtle; and stores the list of centers for X and Y.
'''

class Board:
	'''
	This is the constructor for the Board class.

	The info the Board class will store about itself:
		- self.boardTurtle: A turtle object
		- self.boardMatrix: The matrix that will allow the computer to know where moves were made
		- self.centersList: A list that contains all the values for the centers in a way that can be manipulated to create the coordinates for any square we want
		- self.closestX and self.closestY: These are used to determine where the closest center is to the user input point (the user's click)
		- self.spotOpen: Determines if a spot is open or if it has already been played in
	'''
	def __init__(self):
		self.boardTurtle = Turtle()
		self.boardMatrix = [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]
		self.centersList = [100, 160, 220, 280]
		self.closestX = 0
		self.closestY = 0
		self.spotOpen = True
		
		# Initial turtle settings
		self.boardTurtle.winsize(800, 700, 500, 0)
		self.boardTurtle.tracer(False)
		self.boardTurtle.width(3)
		self.boardTurtle.setWorldCoordinates(-400, -300, 400, 340)
		self.boardTurtle.up()
		self.boardTurtle.onKey(self.quit, "q")
		self.boardTurtle.listen()
		
	# An accessor for closestX
	def getClosestX(self):
		return self.closestX
		
	# An accessor for closestY
	def getClosestY(self):
		return self.closestY

	# This method draws the vertical lines of each grid starting at the location (x, y)
	def drawVerticalLines(self, x, y):
		self.boardTurtle.up()
		self.boardTurtle.goto(x, y)
		self.boardTurtle.down()
		self.boardTurtle.setheading(270)
		self.boardTurtle.forward(240)
		self.boardTurtle.up()
		self.boardTurtle.left(90)
		self.boardTurtle.forward(60)
		self.boardTurtle.down()
		self.boardTurtle.left(90)
		self.boardTurtle.forward(240)
		self.boardTurtle.up()
		self.boardTurtle.right(90)
		self.boardTurtle.forward(60)
		self.boardTurtle.right(90)
		self.boardTurtle.down()
		self.boardTurtle.forward(240)
	
	# This method draws the horizontal lines of each grid starting at the location (x, y)
	def drawHorizontalLines(self, x, y):
		self.boardTurtle.up()
		self.boardTurtle.goto(x, y)
		self.boardTurtle.down()
		self.boardTurtle.setheading(0)
		self.boardTurtle.forward(240)
		self.boardTurtle.up()
		self.boardTurtle.right(90)
		self.boardTurtle.forward(60)
		self.boardTurtle.down()
		self.boardTurtle.right(90)
		self.boardTurtle.forward(240)
		self.boardTurtle.up()
		self.boardTurtle.left(90)
		self.boardTurtle.forward(60)
		self.boardTurtle.left(90)
		self.boardTurtle.down()
		self.boardTurtle.forward(240)
		self.boardTurtle.up()
		
	# This method adds a given roman numeral to a grid for user reference at the location (x, y)
	def addRomanNumerals(self, x, y, numeral):
		self.boardTurtle.goto(x, y)
		self.boardTurtle.write(numeral, font = ("Times New Roman", 48, "normal"))
	
	# This method calls the three previous methods, drawing the boards and roman numerals in the correct locations
	def drawBoard(self):
		# Top left grid
		self.drawVerticalLines(-250, 310)
		self.drawHorizontalLines(-310, 250)
		self.addRomanNumerals(-196, 310, "I")
		# Top right grid
		self.drawVerticalLines(130, 310)
		self.drawHorizontalLines(70, 250)
		self.addRomanNumerals(177, 310, "II")
		# Bottom left grid
		self.drawVerticalLines(-250, -70)
		self.drawHorizontalLines(-310, -130)
		self.addRomanNumerals(-211, -65, "III")
		# Bottom right grid
		self.drawVerticalLines(130, -70)
		self.drawHorizontalLines(70, -130)
		self.addRomanNumerals(170, -65, "IV")
		self.boardTurtle.update()
	
	# This method finds the closest x value and closest y value for a center to the user's click coordinates
	def findSpot(self, x, y):
		if x < 0 and y > 0:
			quadrantMod = [-1, 1]
		elif x > 0 and y > 0:
			quadrantMod = [1, 1]
		elif x < 0 and y < 0:
			quadrantMod = [-1, -1]
		elif x > 0 and y < 0:
			quadrantMod = [1, -1]
		distance = sqrt((x - quadrantMod[0] * self.centersList[0]) ** 2 + (y - quadrantMod[1] * self.centersList[0]) ** 2)
		self.closestX = quadrantMod[0] * self.centersList[0]
		self.closestY = quadrantMod[1] * self.centersList[0]
		for i in range(4):
			for j in range(4):
				if sqrt((x - quadrantMod[0] * self.centersList[i]) ** 2 + (y - quadrantMod[1] * self.centersList[j]) ** 2) < distance:
					distance = sqrt((x - quadrantMod[0] * self.centersList[i]) ** 2 + (y - quadrantMod[1] * self.centersList[j]) ** 2)
					self.closestX = quadrantMod[0] * self.centersList[i]
					self.closestY = quadrantMod[1] * self.centersList[j]
	
	# This method converts x and y coordinates into a location in the board matrix using triple indexes
	def boardMatrixModifier(self, x, y, playerNum):
		# Top left quadrant
		if x < 0 and y > 0:
			gridIndex = 0
			self.centersList.reverse()
			rowIndex = self.centersList.index(abs(y))
			colIndex = self.centersList.index(abs(x))
			self.centersList.reverse()
		# Top right quadrant
		elif x > 0 and y > 0:
			gridIndex = 1
			self.centersList.reverse()
			rowIndex = self.centersList.index(abs(y))
			self.centersList.reverse()
			colIndex = self.centersList.index(abs(x))
		# Bottom left quadrant
		elif x < 0 and y < 0:
			gridIndex = 2
			rowIndex = self.centersList.index(abs(y))
			self.centersList.reverse()
			colIndex = self.centersList.index(abs(x))
			self.centersList.reverse()
		# Bottom right quadrant
		elif x > 0 and y < 0:
			gridIndex = 3
			rowIndex = self.centersList.index(abs(y))
			colIndex = self.centersList.index(abs(x))
		
		# This determines if the spot is open, or if it is taken
		if self.boardMatrix[gridIndex][rowIndex][colIndex] != 0:
			self.spotOpen = False
		else:
			self.spotOpen = True
		
		# Sets the value in the board matrix to 1 or 2 based on which player moved there
		if self.boardMatrix[gridIndex][rowIndex][colIndex] == 0:
			self.boardMatrix[gridIndex][rowIndex][colIndex] = playerNum
	
	# This method is an optional tutorial the player can run at the beginning of the game
	def tutorial(self):
		print
		print "This is the board on which you play the game."
		self.boardTurtle.bgpic("emptyBoard.gif")
		print
		print "The most difficult part of this game is visualizing the cube."
		raw_input("To see how the roman numerals match up to layers of the cube, press enter.")
		self.boardTurtle.bgpic("3DVersion.gif")
		print
		print "In the rest of this tutorial, we will show you the different methods of"
		print "winning."
		print "The first, and simplest way to win is in one row of one grid."
		raw_input("Press enter to see the first example.")
		self.boardTurtle.bgpic("rowInGrid.gif")
		print
		print "The next way to win is in one column of one grid."
		raw_input("Press enter to see an example of this.")
		self.boardTurtle.bgpic("columnInGrid.gif")
		print
		print "The final way to win in one grid is by going diagonally from corner to"
		print "corner in that one grid."
		raw_input("Press enter to see an example of this.")
		self.boardTurtle.bgpic("diagonalInGrid.gif")
		print
		print "The next ways of winning are more complicated. They involve going through"
		print "all the grids. You must be able to visualize the 3D board in order to"
		print "be able to use these. Remember, grid 'I' is the top layer of the board,"
		print "grid 'II', the second, grid 'III', the third, and grid 'IV', the bottom"
		print "layer."
		print "The next way of winning is to go straight down through all four grids."
		raw_input("Press enter to see an example of this.")
		self.boardTurtle.bgpic("lineInLayer.gif")
		print
		print "Another way to win by going through all the grids is diagonally through"
		print "one plane."
		raw_input("Press enter to see an example of this.")
		self.boardTurtle.bgpic("diagonalInLayer.gif")
		print
		print "The final way to win is by going diagonally from one top corner to the"
		print "opposite bottom corner."
		raw_input("Press enter to see an example of this.")
		self.boardTurtle.bgpic("cornerToCorner.gif")
		print
		raw_input("Press enter to exit the tutorial.")
		self.boardTurtle.bgpic("white.gif")
	
	# This method is an infinite loop that runs turtles until the game is over
	def run(self):
		mainloop()
	
	# This method allows us to quit the game on a key command
	def quit(self):
		self.boardTurtle.bye()

'''
The definition for an AI data type.

The AI class implements an artificial intelligence for the game.
'''

class AIPlayer:
	'''
	This is the constructor for the AI class.
	
	The info the AI class will store about itself:
		- self.board: The same board that the game is using, so the AI can decide where to move
		- self.AIBoardMatrix: Makes a deep copy of the boardMatrix so that the computer can modify it to test moves without changing the actual boardMatrix.
		- self.hardMode: Takes player input as to how much AI the computer should use.
		- self.decisionList: The list the AI uses to play randomly.
		- self.x and self.y: The coordinates of the square the AI has chosen to play in.
		- self.iZero, self.jZero and self.kZero: The indexes for the board matrix of the spot the AI has chosen to play in.
		- self.loopNum: References a specific loop in the checkMatrix function so that it knows where it's decision came from.
		- self.ijkVals: The list of four ijk triplets that refer to the four squares that won the game.
		- self.turnNum: Allows it to skip most of the AI thought process on the first turn in order to play faster.
		- self.count1 - self.count8: Counters for the check matrix method. They keep track of occurences of ones or twos in the board matrix.
		- self.ijkList1 - self.ijkList8: Lists that keep track of all the ijk values that have been played in for the current loop. When someone wins, ijkVals is set to the list that contains the four in a row.
	'''
	def __init__(self, board, hardMode = None):
		self.board = board
		self.AIBoardMatrix = deepcopy(self.board.boardMatrix)
		self.hardMode = hardMode
		self.decisionList = [-100, -160, -220, -280, 100, 160, 220, 280] 
		self.x = 0
		self.y = 0
		self.iZero = -1
		self.jZero = -1
		self.kZero = -1
		self.loopNum = 0
		self.ijkVals = []
		self.turnNum = 1
		
		self.count1 = 0
		self.count2 = 0
		self.count3 = 0
		self.count4 = 0
		self.count5 = 0
		self.count6 = 0
		self.count7 = 0
		self.count8 = 0
		self.ijkList1 = []
		self.ijkList2 = []
		self.ijkList3 = []
		self.ijkList4 = []
		self.ijkList5 = []
		self.ijkList6 = []
		self.ijkList7 = []
		self.ijkList8 = []
		
	# An accessor for self.x
	def getX(self):
		return self.x
		
	# An accessor for self.y
	def getY(self):
		return self.y
		
	# This method translates indexes from boardMatrix into x and y coordinates for the turtle to draw.
	def quadrantModifier(self, index1, index2, index3):
		if index1 == 0:
			quadrantMod = [-1, 1]
			self.board.centersList.reverse()
			self.x = quadrantMod[0] * self.board.centersList[index3]
			self.y = quadrantMod[1] * self.board.centersList[index2]
			self.board.centersList.reverse()
		elif index1 == 1:
			quadrantMod = [1, 1]
			self.x = quadrantMod[0] * self.board.centersList[index3]
			self.board.centersList.reverse()
			self.y = quadrantMod[1] * self.board.centersList[index2]
			self.board.centersList.reverse()
		elif index1 == 2:
			quadrantMod = [-1, -1]
			self.board.centersList.reverse()
			self.x = quadrantMod[0] * self.board.centersList[index3]
			self.board.centersList.reverse()
			self.y = quadrantMod[1] * self.board.centersList[index2]
		elif index1 == 3:
			quadrantMod = [1, -1]
			self.x = quadrantMod[0] * self.board.centersList[index3]
			self.y = quadrantMod[1] * self.board.centersList[index2]
	
	# This method checks to see if all of the spots of a given range are taken. This is used as a condition for placeCenters and placeCorners.
	def checkSpots(self, range1, num):
		nonZeroCount = 0
		for i in range1:
			for j in range1:
				for k in range1:
					if self.board.boardMatrix[i][j][k] != 0:
						nonZeroCount = nonZeroCount + 1
		if nonZeroCount == num:
			return False
		else:
			return True
	
	# This method plays randomly in the very center of the cube.
	def placeCenters(self):		
		iRand = randrange(1, 3)
		jRand = randrange(1, 3)
		kRand = randrange(1, 3)
		while self.board.boardMatrix[iRand][jRand][kRand] != 0:
			iRand = randrange(1, 3)
			jRand = randrange(1, 3)
			kRand = randrange(1, 3)
		self.iZero = iRand
		self.jZero = jRand
		self.kZero = kRand
	
	# This method plays randomly in the corners of the cube.
	def placeCorners(self):
		iRand = randrange(0, 4, 3)
		jRand = randrange(0, 4, 3)
		kRand = randrange(0, 4, 3)
		while self.board.boardMatrix[iRand][jRand][kRand] != 0:
			iRand = randrange(0, 4, 3)
			jRand = randrange(0, 4, 3)
			kRand = randrange(0, 4, 3)
		self.iZero = iRand
		self.jZero = jRand
		self.kZero = kRand
		
	# This method checks what the best move would be for the computer by looking ahead one turn, or one computer move and one player move.
	def checkAhead(self):
		self.AIBoardMatrix = deepcopy(self.board.boardMatrix)
		for i in range(4):
			for j in range(4):
				for k in range(4):
					if self.AIBoardMatrix[i][j][k] == 0:
						self.AIBoardMatrix[i][j][k] = 2
						self.checkMatrix(3, self.AIBoardMatrix)
						if self.loopNum == 0:
							for m in range(4):
								for n in range(4):
									for o in range(4):
										if self.AIBoardMatrix[m][n][o] == 0:
											self.AIBoardMatrix[m][n][o] = 1
											self.checkMatrix(3, self.AIBoardMatrix)
											self.AIBoardMatrix[m][n][o] = 0
						self.AIBoardMatrix[i][j][k] = 0

	def recursiveCheckAhead(self, win, board, player, depth):
		if depth == 0:
			return
		for i in range(4):
			for j in range(4):
				for k in range(4):
					if board[i][j][k] == 0:
						board[i][j][k] == player
						if self.checkMatrix(4, board):
							return depth, True
						else:
							self.checkMatrix(3, board)
	
	# This method resets the counts and ijkLists.
	def countAndListReset(self):
		self.count1 = 0
		self.count2 = 0
		self.count3 = 0
		self.count4 = 0
		self.count5 = 0
		self.count6 = 0
		self.count7 = 0
		self.count8 = 0
		self.ijkList1 = []
		self.ijkList2 = []
		self.ijkList3 = []
		self.ijkList4 = []
		self.ijkList5 = []
		self.ijkList6 = []
		self.ijkList7 = []
		self.ijkList8 = []
	
	# This method appends the i, j, and k values to a given ijkList
	def ijkListAppend(self, list, val1, val2, val3):
		list.append(val1)
		list.append(val2)
		list.append(val3)
	
	# This method sets ijkVals to whichever list contains 4 in a row.
	def setijkVals(self):
		if self.count1 == 4:
			self.ijkVals = self.ijkList1
			return True
		if self.count2 == 4:
			self.ijkVals = self.ijkList2
			return True
		if self.count3 == 4:
			self.ijkVals = self.ijkList3
			return True
		if self.count4 == 4:
			self.ijkVals = self.ijkList4
			return True
		if self.count5 == 4:
			self.ijkVals = self.ijkList5
			return True
		if self.count6 == 4:
			self.ijkVals = self.ijkList6
			return True
		if self.count7 == 4:
			self.ijkVals = self.ijkList7
			return True
		if self.count8 == 4:
			self.ijkVals = self.ijkList8
			return True
	
	# This method checks to see whether there are three or four in a row anywhere in the cube.
	def checkMatrix(self, num, board):
		# 3 or 4 in a row diagonally through all rows and all grids
		# We used 3 four loops to iterate through all of the spots in the matrix in a specific order
		# We reset the counts and lists before the innermost iteration so that the counts for a given inner iteration (which refers to single spots) start at zero
		self.countAndListReset()
		for i in range(4):
			if board[i][i][i] == 1:
				self.count1 = self.count1 + 1
				self.ijkListAppend(self.ijkList1, i, i, i)
			if board[i][i][i] == 2:
				self.count2 = self.count2 + 1
				self.ijkListAppend(self.ijkList2, i, i, i)
			if board[i][i][3-i] == 1:
				self.count3 = self.count3 + 1
				self.ijkListAppend(self.ijkList3, i, i, 3-i)
			if board[i][i][3-i] == 2:
				self.count4 = self.count4 + 1
				self.ijkListAppend(self.ijkList4, i, i, 3-i)
			if board[i][3-i][i] == 1:
				self.count5 = self.count5 + 1
				self.ijkListAppend(self.ijkList5, i, 3-i, i)
			if board[i][3-i][i] == 2:
				self.count6 = self.count6 + 1
				self.ijkListAppend(self.ijkList6, i, 3-i, i)
			if board[i][3-i][3-i] == 1:
				self.count7 = self.count7 + 1
				self.ijkListAppend(self.ijkList7, i, 3-i, 3-i)
			if board[i][3-i][3-i] == 2:
				self.count8 = self.count8 + 1
				self.ijkListAppend(self.ijkList8, i, 3-i, 3-i)
			# If we are looking for 3 in a row
			if num == 3:
				# If there are three 2's in a row, and the final spot is open. We had it count 2's first so that it would win before blocking.
				if self.count2 == num and self.count1 + self.count2 != 4:
					for l in range(4):
						# Finds the open spot in the row, and records the i, j, and k values of that spot to pass to other methods
						if board[l][l][l] == 0:
							self.iZero = l
							self.loopNum = 10
							return
				if self.count4 == num and self.count3 + self.count4 != 4:
					for l in range(4):
						if board[l][l][3-l] == 0:
							self.iZero = l
							self.loopNum = 11
							return
				if self.count6 == num and self.count5 + self.count6 != 4:
					for l in range(4):
						if board[l][3-l][l] == 0:
							self.iZero = l
							self.loopNum = 12
							return
				if self.count8 == num and self.count1 + self.count2 != 4:
					for l in range(4):
						if board[l][3-l][3-l] == 0:
							self.iZero = l
							self.loopNum = 13
							return
				if self.count1 == num and self.count1 + self.count2 != 4:
					for l in range(4):
						if board[l][l][l] == 0:
							self.iZero = l
							self.loopNum = 10
				if self.count3 == num and self.count3 + self.count4 != 4:
					for l in range(4):
						if board[l][l][3-l] == 0:
							self.iZero = l
							self.loopNum = 11
				if self.count5 == num and self.count5 + self.count6 != 4:
					for l in range(4):
						if board[l][3-l][l] == 0:
							self.iZero = l
							self.loopNum = 12
				if self.count7 == num and self.count1 + self.count2 != 4:
					for l in range(4):
						if board[l][3-l][3-l] == 0:
							self.iZero = l
							self.loopNum = 13
			# If there are 4 in the row and we are looking for 4 in a row
			if self.count1 == num == 4 or self.count2 == num == 4 or self.count3 == num == 4 or self.count4 == num == 4 or self.count5 == num == 4 or self.count6 == num == 4 or self.count7 == num == 4 or self.count8 == num == 4:	 
				return self.setijkVals()
		# 3 or 4 in a row diagonally down one row or column through all four grids
		for i in range(4):
			self.countAndListReset()
			for j in range(4):
				if board[j][i][j] == 1:
					self.count1 = self.count1 + 1
					self.ijkListAppend(self.ijkList1, j, i, j)
				if board[j][i][j] == 2:
					self.count2 = self.count2 + 1
					self.ijkListAppend(self.ijkList2, j, i, j)
				if board[j][i][3-j] == 1:
					self.count3 = self.count3 + 1
					self.ijkListAppend(self.ijkList3, j, i, 3-j)
				if board[j][i][3-j] == 2:
					self.count4 = self.count4 + 1
					self.ijkListAppend(self.ijkList4, j, i, 3-j)
				if board[j][j][i] == 1:
					self.count5 = self.count5 + 1
					self.ijkListAppend(self.ijkList5, j, j, i)
				if board[j][j][i] == 2:
					self.count6 = self.count6 + 1
					self.ijkListAppend(self.ijkList6, j, j, i)
				if board[j][3-j][i] == 1:
					self.count7 = self.count7 + 1
					self.ijkListAppend(self.ijkList7, j, 3-j, i)
				if board[j][3-j][i] == 2:
					self.count8 = self.count8 + 1
					self.ijkListAppend(self.ijkList8, j, 3-j, i)
				if num == 3:
					if self.count2 == num and self.count1 + self.count2 != 4:
						for l in range(4):
							if board[l][i][l] == 0:
								self.iZero = i
								self.jZero = l
								self.loopNum = 6
								return
					if self.count4 == num and self.count3 + self.count4 != 4:
						for l in range(4):
							if board[l][i][3-l] == 0:
								self.iZero = i
								self.jZero = l
								self.loopNum = 7
								return
					if self.count6 == num and self.count5 + self.count6 != 4:
						for l in range(4):
							if board[l][l][i] == 0:
								self.iZero = i
								self.jZero = l
								self.loopNum = 8
								return
					if self.count8 == num and self.count7 + self.count8 != 4:
						for l in range(4):
							if board[l][3-l][i] == 0:
								self.iZero = i
								self.jZero = l
								self.loopNum = 9
								return
					if self.count1 == num and self.count1 + self.count2 != 4:
						for l in range(4):
							if board[l][i][l] == 0:
								self.iZero = i
								self.jZero = l
								self.loopNum = 6
					if self.count3 == num and self.count3 + self.count4 != 4:
						for l in range(4):
							if board[l][i][3-l] == 0:
								self.iZero = i
								self.jZero = l
								self.loopNum = 7
					if self.count5 == num and self.count5 + self.count6 != 4:
						for l in range(4):
							if board[l][l][i] == 0:
								self.iZero = i
								self.jZero = l
								self.loopNum = 8
					if self.count7 == num and self.count1 + self.count2 != 4:
						for l in range(4):
							if board[l][3-l][i] == 0:
								self.iZero = i
								self.jZero = l
								self.loopNum = 9
				if self.count1 == num == 4 or self.count2 == num == 4 or self.count3 == num == 4 or self.count4 == num == 4 or self.count5 == num == 4 or self.count6 == num == 4 or self.count7 == num == 4 or self.count8 == num == 4:	 
					 return self.setijkVals()
		# 3 or 4 in a row straight down through all four grids
		for i in range(4):
			for j in range(4):
				self.countAndListReset()
				for k in range(4):
					if board[k][j][i] == 1:
						self.count1 = self.count1 + 1
						self.ijkListAppend(self.ijkList1, k, j, i)
					if board[k][j][i] == 2:
						self.count2 = self.count2 + 1
						self.ijkListAppend(self.ijkList2, k, j, i)
					if num == 3:
						if self.count2 == num and self.count1 + self.count2 != 4:
							for l in range(4):
								if board[l][j][i] == 0:
									self.iZero = i
									self.jZero = j
									self.kZero = l
									self.loopNum = 5
									return
						if self.count1 == num and self.count1 + self.count2 != 4:
							for l in range(4):
								if board[l][j][i] == 0:
									self.iZero = i
									self.jZero = j
									self.kZero = l
									self.loopNum = 5
				if self.count1 == num == 4 or self.count2 == num == 4:	 
					 return self.setijkVals()
		# 3 or 4 in a row diagonally across one grid
		for i in range(4):
			self.countAndListReset()
			for j in range(4):
				if board[i][j][j] == 1:
					self.count1 = self.count1 + 1
					self.ijkListAppend(self.ijkList1, i, j, j)
				if board[i][j][j] == 2:
					self.count2 = self.count2 + 1
					self.ijkListAppend(self.ijkList2, i, j, j)
				if board[i][j][3-j] == 1:
					self.count3 = self.count3 + 1
					self.ijkListAppend(self.ijkList3, i, j, 3-j)
				if board[i][j][3-j] == 2:
					self.count4 = self.count4 + 1
					self.ijkListAppend(self.ijkList4, i, j, 3-j)
				if num == 3:
					if self.count2 == num and self.count1 + self.count2 != 4:
						for l in range(4):
							if board[i][l][l] == 0:
								self.iZero = i
								self.jZero = l
								self.loopNum = 3
								return
					if self.count4 == num and self.count3 + self.count4 != 4:
						for l in range(4):
							if board[i][l][3-l] == 0:
								self.iZero = i
								self.jZero = l
								self.loopNum = 4
								return				
					if self.count1 == num and self.count1 + self.count2 != 4:
						for l in range(4):
							if board[i][l][l] == 0:
								self.iZero = i
								self.jZero = l
								self.loopNum = 3
					if self.count3 == num and self.count3 + self.count4 != 4:
						for l in range(4):
							if board[i][l][3-l] == 0:
								self.iZero = i
								self.jZero = l
								self.loopNum = 4
				if self.count1 == num == 4 or self.count2 == num == 4 or self.count3 == num == 4 or self.count4 == num == 4:	 
					 return self.setijkVals()
		# 3 or 4 in a row in one column of one grid
		for i in range(4):
			for j in range(4):
				self.countAndListReset()
				for k in range(4):
					if board[i][k][j] == 1:
						self.count1 = self.count1 + 1
						self.ijkListAppend(self.ijkList1, i, k, j)
					if board[i][k][j] == 2:
						self.count2 = self.count2 + 1
						self.ijkListAppend(self.ijkList2, i, k, j)
					if num == 3:
						if self.count2 == num and self.count1 + self.count2 != 4:
							for l in range(4):
								if board[i][l][j] == 0:
									self.iZero = i
									self.kZero = l
									self.jZero = j
									self.loopNum = 2
									return
						elif self.count1 == num and self.count1 + self.count2 != 4:
							for l in range(4):
								if board[i][l][j] == 0:
									self.iZero = i
									self.kZero = l
									self.jZero = j
									self.loopNum = 2
				if self.count1 == num == 4 or self.count2 == num == 4:	 
					 return self.setijkVals()
		# 3 or 4 in a row in one row of one grid
		for i in range(4):
			for j in range(4):
				self.countAndListReset()
				for k in range(4):
					if board[i][j][k] == 1:
						self.count1 = self.count1 + 1
						self.ijkListAppend(self.ijkList1, i, j, k)
					if board[i][j][k] == 2:
						self.count2 = self.count2 + 1
						self.ijkListAppend(self.ijkList2, i, j, k)
					if num == 3:
						if self.count2 == num and self.count1 + self.count2 != 4:
							for l in range(4):
								if board[i][j][l] == 0:
									self.iZero = i
									self.jZero = j
									self.kZero = l
									self.loopNum = 1
									return
						elif self.count1 == num and self.count1 + self.count2 != 4:
							for l in range(4):
								if board[i][j][l] == 0:
									self.iZero = i
									self.jZero = j
									self.kZero = l
									self.loopNum = 1
					if self.count1 == num == 4 or self.count2 == num == 4:
						return self.setijkVals()
		return False
	
	# This method is how the AI chooses where to play.
	def decision(self):
		# It will start out by placing in a center. It skips most of the AI process because it doesn't need to check to see if there's anything to block on the first turn.
		if self.turnNum == 1:
			self.placeCenters()
			self.quadrantModifier(self.iZero, self.jZero, self.kZero)
			self.turnNum = 2
		else:
			# If it is playing in hard mode, it needs to check ahead a turn.
			if self.hardMode == True:
				self.checkAhead()
			# If it is playing in easy mode, it only responds based on what the board currently looks like.
			else:
				self.checkMatrix(3, self.board.boardMatrix)
			# These statements allow the computer to block the player if they get three in a row, and to win if it gets three in a row. They check which loop they got their i, j, k coordinates from and if the spot is open. It then modifies the matrix and resets the loop number for the next turn.
			if self.loopNum == 1 and self.board.boardMatrix[self.iZero][self.jZero][self.kZero] == 0:
				self.quadrantModifier(self.iZero, self.jZero, self.kZero)
				self.loopNum = 0
			elif self.loopNum == 2 and self.board.boardMatrix[self.iZero][self.kZero][self.jZero] == 0:
				self.quadrantModifier(self.iZero, self.kZero, self.jZero)
				self.loopNum = 0
			elif self.loopNum == 3 and self.board.boardMatrix[self.iZero][self.jZero][self.jZero] == 0:
				self.quadrantModifier(self.iZero, self.jZero, self.jZero)
				self.loopNum = 0
			elif self.loopNum == 4 and self.board.boardMatrix[self.iZero][self.jZero][3-self.jZero] == 0:
				self.quadrantModifier(self.iZero, self.jZero, 3-self.jZero)
				self.loopNum = 0
			elif self.loopNum == 5 and self.board.boardMatrix[self.kZero][self.jZero][self.iZero] == 0:
				self.quadrantModifier(self.kZero, self.jZero, self.iZero)
				self.loopNum = 0
			elif self.loopNum == 6 and self.board.boardMatrix[self.jZero][self.iZero][self.jZero] == 0:
				self.quadrantModifier(self.jZero, self.iZero, self.jZero)
				self.loopNum = 0
			elif self.loopNum == 7 and self.board.boardMatrix[self.jZero][self.iZero][3-self.jZero] == 0:
				self.quadrantModifier(self.jZero, self.iZero, 3-self.jZero)
				self.loopNum = 0
			elif self.loopNum == 8 and self.board.boardMatrix[self.jZero][self.jZero][self.iZero] == 0:
				self.quadrantModifier(self.jZero, self.jZero, self.iZero)
				self.loopNum = 0
			elif self.loopNum == 9 and self.board.boardMatrix[self.jZero][3-self.jZero][self.iZero] == 0:
				self.quadrantModifier(self.jZero, 3-self.jZero, self.iZero)
				self.loopNum = 0
			elif self.loopNum == 10 and self.board.boardMatrix[self.iZero][self.iZero][self.iZero] == 0:
				self.quadrantModifier(self.iZero, self.iZero, self.iZero)
				self.loopNum = 0
			elif self.loopNum == 11 and self.board.boardMatrix[self.iZero][self.iZero][3-self.iZero] == 0:
				self.quadrantModifier(self.iZero, self.iZero, 3-self.iZero)
				self.loopNum = 0
			elif self.loopNum == 12 and self.board.boardMatrix[self.iZero][3-self.iZero][self.iZero] == 0:
				self.quadrantModifier(self.iZero, 3-self.iZero, self.iZero)
				self.loopNum = 0
			elif self.loopNum == 13 and			self.board.boardMatrix[self.iZero][3-self.iZero][3-self.iZero] == 0:
				self.quadrantModifier(self.iZero, 3-self.iZero, 3-self.iZero)
				self.loopNum = 0
			# This statement checks to see if there are still centers in grid II or III it hasn't played in, and if so, it will play in them. Then it checks to see if there are corners in grids I or IV it hasn't played in.
			elif self.checkSpots(range(1, 3), 8) == True:
				self.placeCenters()
				self.quadrantModifier(self.iZero, self.jZero, self.kZero)
			elif self.checkSpots(range(0, 4, 3), 8) == True:
				self.placeCorners()
				self.quadrantModifier(self.iZero, self.jZero, self.kZero)
			# If all else fails, it will place randomly.
			else:
				self.x = self.decisionList[randrange(0, 7)]
				self.y = self.decisionList[randrange(0, 7)]
				self.board.boardMatrixModifier(self.x, self.y, 0)
				while self.board.spotOpen == False:
					self.x = self.decisionList[randrange(0, 7)]
					self.y = self.decisionList[randrange(0, 7)]
					self.board.boardMatrixModifier(self.x, self.y, 0)

'''
The definition for a Game data type.

The Game class sets up and runs a game, either between one player and the AI, or two players.
'''

class Game:
	'''
	This is the constructor for the Game class.
	
	The info the Game class will store about itself:
		- self.board: A board object, the same one that's used in the AI class
		- self.gameEnded: Allows us to tell whether the game is over or not by changing whether it is True or False
		- self.AI: An AI player object
		- self.againstAI: Tells the computer whether to implement one player mode (against the AI) or two player mode
	'''
	def __init__(self, board, AI, againstAI = True):
		self.board = board
		self.gameEnded = False
		self.AI = AI
		self.againstAI = againstAI
		
		self.board.boardTurtle.onClick(self.drawX)

	# This method draws an X at the location (x, y), calls boardMatrixModifier to modify the matrix, calls checkMatrix to see if the game is over, and switches turtles onClick to drawO, or calls the AI.
	def drawX(self, x, y):
		self.drawBox("white")
		self.board.findSpot(x, y)
		self.board.boardMatrixModifier(self.board.closestX, self.board.closestY, 1)
		if self.board.spotOpen == True:
			self.board.boardTurtle.goto(self.board.closestX, self.board.closestY)
			self.board.boardTurtle.setheading(-45)
			self.board.boardTurtle.backward(28)
			self.board.boardTurtle.down()
			self.board.boardTurtle.forward(56)
			self.board.boardTurtle.up()
			self.board.boardTurtle.setheading(90)
			self.board.boardTurtle.forward(40)
			self.board.boardTurtle.down()
			self.board.boardTurtle.setheading(225)
			self.board.boardTurtle.forward(56)
			self.board.boardTurtle.up()
			self.gameEnded = self.AI.checkMatrix(4, self.board.boardMatrix)
			if self.gameEnded == True:
				self.board.boardTurtle.onClick(None)
				self.board.boardTurtle.goto(-100, 0)
				self.board.boardTurtle.write("Player 1 wins!", font = ("Ariel", 30, "normal"))
				self.board.boardTurtle.setheading(0)
				self.highlightWin()
			elif self.AI.checkSpots(range(4), 64) == False:
				self.board.boardTurtle.onClick(None)
				self.board.boardTurtle.goto(-100, 0)
				self.board.boardTurtle.write("NOBODY WINS", font = ("Ariel", 30, "normal"))
			else:
				if self.againstAI == False:
					self.board.boardTurtle.onClick(self.drawO)
				else:
					self.AI.decision()
					self.drawO(self.AI.getX(), self.AI.getY())
		
	# This method does the same thing as drawX, but it places O's, rather than X's, and doesn't ever call AI, because AI is always O's.
	def drawO(self, x, y):
		self.board.findSpot(x, y)
		self.board.boardMatrixModifier(self.board.closestX, self.board.closestY, 2)
		if self.board.spotOpen == True:
			self.board.boardTurtle.goto(self.board.closestX, self.board.closestY + 20)
			self.board.boardTurtle.setheading(180)
			self.board.boardTurtle.down()
			self.board.boardTurtle.circle(20)
			self.board.boardTurtle.up()
			self.board.boardTurtle.onClick(self.drawX)
			if self.againstAI == True:
				self.drawBox("blue")
			self.gameEnded = self.AI.checkMatrix(4, self.board.boardMatrix)
			if self.gameEnded == True:
				self.board.boardTurtle.onClick(None)
				if self.againstAI == False:
					self.board.boardTurtle.goto(-100, 0)
					self.board.boardTurtle.write("Player 2 wins!", font = ("Ariel", 30, "normal"))
				elif self.againstAI == True:
					self.board.boardTurtle.goto(-145, 0)
					self.board.boardTurtle.write("The Computer wins!", font = ("Ariel", 30, "normal"))
				self.highlightWin()
			elif self.AI.checkSpots(range(4), 64) == False:
				self.board.boardTurtle.onClick(None)
				self.board.boardTurtle.goto(-100, 0)
				self.board.boardTurtle.write("NOBODY WINS", font = ("Ariel", 30, "normal"))
	
	# This draws a box around the current square of a given color. This allows us to show where the AI's most recent move was and highlight how someone won the game.
	def drawBox(self, color):
		self.board.boardTurtle.goto(self.AI.x, self.AI.y)
		self.board.boardTurtle.forward(26)
		self.board.boardTurtle.right(90)
		self.board.boardTurtle.forward(26)
		self.board.boardTurtle.color(color)
		self.board.boardTurtle.down()
		for j in range(4):
			self.board.boardTurtle.right(90)
			self.board.boardTurtle.forward(52)
		self.board.boardTurtle.up()
		self.board.boardTurtle.color("black")
	
	# Calls drawBox to highlight the boxes that create the four in a row that won the game.
	def highlightWin(self):
		for i in range(0, 12, 3):
			self.AI.quadrantModifier(self.AI.ijkVals[i], self.AI.ijkVals[i+1], self.AI.ijkVals[i+2])
			self.drawBox("red")

# This function prints the instructions in terminal, asks for user input on whether they want to see the tutorial, how many players, what level computer they want to play, if applicable, and whether they want to go first or second when playing against the computer. It then runs the game.
def main():
	print
	print "Instructions:"
	print
	print "This game is a 3D version of tic-tac-toe. Since it is 3D, it has a 4x4x4 board,"
	print "rather than the traditional 3x3 tic-tac-toe board. This board is represented in" 
	print "two dimensions, with four 4x4 boards, labeled with roman numerals ('I' being"
	print "the first level of the cube, and 'IV' being the bottom level). In order to win,"
	print "you have to get four X's or O's in a row. These can be any four in a row in the"
	print "cube, including going through all the grids. To play, click where you want"
	print "to go."
	print
	tutorialInputList = ["yes", "y", "no", "n"]
	tutorialInput = raw_input("Would you like to see the full tutorial? ").lower()
	while tutorialInput not in tutorialInputList:
		print
		print "Invalid input. Please input 'yes' or 'no'."
		print
		tutorialInput = raw_input("Would you like to see the full tutorial? ").lower()
	if tutorialInput == "yes" or tutorialInput == "y":
		board = Board()
		board.tutorial()
	print
	modeInputList = ["one", "one player", "1", "two", "two player", "two players", "2"]
	modeInput = raw_input("Do you want to play one player or two player mode? ").lower()
	while modeInput not in modeInputList:
		print
		print "Invalid input. Please input '1' or '2'."
		print
		modeInput = raw_input("Do you want to play one player or two player mode? ").lower()
	board = Board()
	if modeInput == "one" or modeInput == "one player" or modeInput == "1":
		levelInputList = ["easy", "e", "hard", "h"]
		print
		levelInput = raw_input("Would you like to play easy or hard mode? ").lower()
		while levelInput not in levelInputList:
			print
			print "Invalid input. Please input 'easy' or 'hard'."
			print
			levelInput = raw_input("Would you like to play easy or hard mode? ").lower()
		if levelInput == "easy" or levelInput == "e":
			AI = AIPlayer(board, False)
		elif levelInput == "hard" or levelInput == "h":
			AI = AIPlayer(board, True)
		orderInputList = ["first", "1", "1st", "second", "2", "2nd"]
		print
		orderInput = raw_input("Would you like to go first or second? ").lower()
		while orderInput not in orderInputList:
			print
			print "Invalid input. Please input '1' or '2'."
			print
			orderInput = raw_input("Would you like to go first or second? ").lower()
		if orderInput == "first" or orderInput == "1" or orderInput == "1st":
			game = Game(board, AI)
			turnOrder = 1
		elif orderInput == "second" or orderInput == "2" or orderInput == "2nd":
			game = Game(board, AI)
			turnOrder = 2
		print
		print "WARNING: it might take the AI a few seconds to place a move. Don't panic."
		print "Be patient. ONLY CLICK ONCE. It did recognize your click."
	elif modeInput == "two" or modeInput == "two player" or modeInput == "two players" or modeInput == "2":
		AI = AIPlayer(board)
		game = Game(board, AI, False)
		turnOrder = 0
	print
	print "Press 'q' to quit."
	board.drawBoard()
	if turnOrder == 2:
		game.AI.decision()
		game.drawO(game.AI.getX(), game.AI.getY())
	board.run()
	
main()