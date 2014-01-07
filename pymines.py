#!/usr/bin/env python
# coding=utf-8

# Mine Sweeper Clone made With Python and Pygame

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import pygame
import random
from pygame.locals import *

# Pygame related constants
FPS      = 30
NUMMINES = 4

BOARDWIDTH   = 4
BOARDHEIGHT  = 4
FIELDSIZE = 20
GAPSIZE = 10
PANELWIDHT  = int(BOARDWIDTH * (FIELDSIZE + GAPSIZE) - GAPSIZE)
PANELHEIGHT = 20
XMARGIN = 3
YMARGIN = 3
WINDOWWIDHT  = (2 * XMARGIN) + PANELWIDHT
WINDOWHEIGHT = (2 * YMARGIN) + PANELHEIGHT + (BOARDHEIGHT * (FIELDSIZE + GAPSIZE))
MINERADIUS = 5

MINE = -1
WON  =  1
LOST = -1

# Colors      R    G    B
BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
BLUE     = (  0,   0, 255)
GRAY     = (100, 100, 100)

BGCOLOR          = BLACK
CLOSEDFIELDCOLOR = GRAY
OPENFIELDCOLOR   = WHITE
MINEBGCOLOR      = RED
MINECOLOR        = BLACK
PANELBGCOLOR     = BLUE

class MineBoard():
	"""Mine Sweeper board class, used for playing Py-Mines game.

	This class defines a board of the game Mine Sweeper, with
	methods useful for the game itself."""

	def __init__(self, rows, cols, numMines):
		"""Initialize an instance."""

		self.rows = rows
		self.cols = cols

		self.__createMainMatrix(numMines)
		self.__createHiddenMatrix()

	def openField(self, x, y):
		"""Open a field on the board.

		Return LOST if the game a mine was opened,
		WON if the game was won and 0 otherwise."""

		if self.isMine(x, y):
			self.__gameLost()
			return LOST
		else:
			self.hidden[x][y] = False
			if self.main[x][y] == 0:
				self.__openSurroundingFields(x, y)
			if self.hasWon():
				return WON
		return 0

	def hasWon(self):
		"""Check if the player won the game."""

		for x in range(self.rows):
			for y in range(self.cols):
				if self.isHidden(x, y) and not self.isMine(x, y):
					return False
		return True

	def isHidden(self, x, y):
		"""Check if the field at the (x,y) coordinate is hidden.

		Returns True if it's hidden and False otherwise."""

		return self.hidden[x][y]

	def isMine (self, x, y):
		"""Check if the field at the (x,y) coordinate is a mine.

		Returns True if it's a mine and False otherwise."""

		return self.main[x][y] == MINE

	def __createMainMatrix(self, numMines):
		"""Creates a board matrix and mines list.

		Creates matrix with mines in certain fields and numbers
		on the others. These numbers indicates how many mines
		are surrounding that field. Also creates a list with
		coordinates tuples, indicating mines coodinates
		
		This method is not intended to be used by the client,
		it's just for internal use by other methods of this
		class.

		minesRows, minesCols and self.mines feels redundant.
		This method will get a revision after version 1.0."""

		self.main = []
		for i in range(self.rows):
			line = []
			for j in range(self.cols):
				line.append(0)
			self.main.append(line)

		# Lists of coordinates
		minesRows = []
		minesCols = []

		# Create random coordinates of mines
		for i in range(numMines):
			valid = False
			while not valid:
				x = random.randint(0, self.rows - 1)
				y = random.randint(0, self.cols - 1)
				valid = True
				for i in range(len(minesRows)):
					if x == minesRows[i] and y == minesCols[i]:
						valid = False
			minesRows.append(x)
			minesCols.append(y)

		# Plot mines in "main" matrix and make mines list
		self.mines = []
		for i in range(numMines):
			x, y = minesRows[i], minesCols[i]
			self.main[x][y] = MINE
			self.mines.append((x, y))

		# Generate the numbers on the board, given the mines
		for x in range(self.rows):
			for y in range(self.cols):
				if not self.isMine(x, y):
					self.main[x][y] = self.__surroundingMines(x, y)

	def __createHiddenMatrix(self):
		"""Creates a hidden matrix

		Creates a matrix indicating (with boolean values)
		which fields are closed.

		This method is not intended to be used by the client,
		it's just for internal use by other methods of this
		class."""

		self.hidden = []
		for i in range(self.rows):
			line = []
			for j in range(self.cols):
				line.append(True)
			self.hidden.append(line)

	def __surroundingMines(self, x, y):
		"""How many mines surround a field.

		This method considers that field (x,y) isn't a mine.

		This method is not intended to be used by the client,
		it's just for internal use by other methods of this
		class."""

		# Count the surround mines
		count = 0
		for i in range(-1, 2):
			for j in range(-1, 2):
				# Check if x+i and y+j stays inside the board
				if (x + i >= 0 and x + i < self.rows) and (y + j >= 0 and y + j < self.cols):
					if self.isMine(x + i, y + j):
						count += 1

		return count

	def __gameLost(self):
		"""Take actions after opening a field containing a mine."""
		self.__openAllFields()

	def __openSurroundingFields(self, x, y):
		"""Open surrounding fields of a specified cordinate"""
		for i in range(-1, 2):
			for j in range(-1, 2):
				# Check if x+i and y+j stays inside the board
				if (x + i >= 0 and x + i < self.rows) and (y + j >= 0 and y + j < self.cols):
					self.openField(x + i, y + j)

	def __openAllFields(self):
		for i in range(self.rows):
			for j in range(self.cols):
				self.hidden[i][j] = False


def main():
	# Declare global variables
	global DISPLAY, FONT, PANELFONT, FPSCLOCK

	# Start Pygame
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAY  = pygame.display.set_mode((WINDOWWIDHT, WINDOWHEIGHT))
	pygame.display.set_caption("Memory Game")

	# Fonts
	FONT = pygame.font.Font('freesansbold.ttf', 11)
	PANELFONT = pygame.font.Font('freesansbold.ttf', 11)

	# Start board
	board = MineBoard(BOARDHEIGHT, BOARDWIDTH, NUMMINES)

	# Print the board on console, for debugging
	for line in board.main:
		print(line)

	# Main game loop
	while True:
		mouseClicked = False
		status = 0

		# Event-handling loop
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				terminate()
			elif event.type == MOUSEBUTTONUP:
				mouseX, mouseY = event.pos
				mouseClicked = True

		if mouseClicked:
			# Get coordinates of the field that the cursor is pointing
			fieldX, fieldY = getFieldAtPixel(mouseX, mouseY)

			if (fieldX, fieldY) != (None, None):
				# Open field and store returned status
				status = board.openField(fieldX, fieldY)

		drawBoard(board, status)

		if status == WON or status == LOST:
			# If you won or lost the game, it is reseted
			pygame.display.update()
			pygame.time.wait(2000)
			board = MineBoard(BOARDHEIGHT, BOARDWIDTH, NUMMINES)

		# Redraw the screen and wait for the clock tick
		pygame.display.update()
		FPSCLOCK.tick(FPS)

def getFieldAtPixel(mouseX, mouseY):
	"""What field is at pixel's coordinates (x, y)"""

	for x in range(BOARDWIDTH):
		for y in range(BOARDHEIGHT):
			left, top = getLeftTopCoordsOfField(x, y)
			fieldRect = pygame.Rect(left, top, FIELDSIZE, FIELDSIZE)

			# If the point (x, y) collides with this box, then, this is the box under this pixel!
			if fieldRect.collidepoint(mouseX, mouseY):
				return (x, y)

	# If no box collides with (x, y)
	return (None, None)

def getLeftTopCoordsOfField(fieldX, fieldY):
	left = XMARGIN + (fieldX * (FIELDSIZE + GAPSIZE))
	top = YMARGIN + (PANELHEIGHT + GAPSIZE) + (fieldY * (FIELDSIZE + GAPSIZE))

	return (left, top)

def drawBoard(board, status):
	"""Draw the game board on screen."""
	# Draw background
	DISPLAY.fill(BGCOLOR)

	# Draw fields
	for x in range(board.rows):
		for y in range(board.cols):
			drawField(board, x, y)

	# Draw the panel
	drawPanel(board, status)

def drawField(board, x, y):
	left, top = getLeftTopCoordsOfField(x, y)

	if board.isHidden(x, y):
		# Draw closed field
		pygame.draw.rect(DISPLAY, CLOSEDFIELDCOLOR, (left, top, FIELDSIZE, FIELDSIZE))
	elif board.isMine(x, y):
		# Draw mine
		pygame.draw.rect(DISPLAY, MINEBGCOLOR, (left, top, FIELDSIZE, FIELDSIZE))
		pygame.draw.circle(DISPLAY, MINECOLOR, (int(left + (FIELDSIZE/2)), int(top + (FIELDSIZE/2))), MINERADIUS, 0)
	elif board.main[x][y] == 0:
		# Draw opened and empty field
		pygame.draw.rect(DISPLAY, OPENFIELDCOLOR, (left, top, FIELDSIZE, FIELDSIZE))
	else:
		# Draw opened field with a number on it
		pygame.draw.rect(DISPLAY, OPENFIELDCOLOR, (left, top, FIELDSIZE, FIELDSIZE))
		textSurfaceObj = FONT.render(str(board.main[x][y]), True, BLACK)
		textRectObj = textSurfaceObj.get_rect()
		textRectObj.center = (left + (FIELDSIZE/2), top + (FIELDSIZE/2))
		DISPLAY.blit(textSurfaceObj, textRectObj)


def drawPanel(board, status):
	"""Draw panel on DISPLAY based on the status. """
	left, top = XMARGIN, YMARGIN

	pygame.draw.rect(DISPLAY, PANELBGCOLOR, (left, top, PANELWIDHT, PANELHEIGHT))

	if status == WON or status == LOST:
		# Draw message

		if status == WON:
			textSurfaceObj = PANELFONT.render("WON!", True, WHITE)
		else:
			textSurfaceObj = PANELFONT.render("YOU LOST", True, WHITE)

		textRectObj = textSurfaceObj.get_rect()
		textRectObj.center = (left + (PANELWIDHT/2), top + (PANELHEIGHT/2))
		DISPLAY.blit(textSurfaceObj, textRectObj)

def terminate():
	pygame.quit() # Quit PyGame
	sys.exit() # Exit program

if __name__ == "__main__":
	main()