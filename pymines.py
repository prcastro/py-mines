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

# Constants
MINE = -1

class MineBoard():
	"""Mine Sweeper board class, used for playing Py-Mines game.

	This class defines a board of the game Mine Sweeper, with
	methods useful for the game itself."""

	def __init__(self, rows, cols, numMines):
		"""Initialize an instance."""

		self.__createMinesMatrix(rows, cols, numMines)
		self.__createHiddenMatrix(rows, cols)

		print(self.mines)
		

	def isHidden(self, x, y):
		"""Check if the field at the (x,y) coordinate is hidden.

		Returns True if it's hidden and False otherwise."""

		return self.hidden[x][y]

	def isMine (self, x, y):
		"""Check if the field at the (x,y) coordinate is a mine.

		Returns True if it's a mine and False otherwise."""

		return self.mines[x][y] == MINE

	def drawBoard(self):
		"""Draw the board on screen."""

		pass

	def hasWon(self):
		"""Check if the player won the game."""

		for x in len(self.hidden):
			for y in len(self.hidden[0]):
				if self.hidden[x][y]:
					return False
		return True

	def __createMinesMatrix(self, rows, cols, numMines):
		"""Creates a mines matrix.

		Creates matrix with mines in certain fields and numbers
		on the others. These numbers indicates how many mines
		are surrounding that field.
		
		This method is not intended to be used by the client,
		it's just for internal use by other methods of this
		class."""

		self.mines = []
		for i in range(rows):
			line = []
			for j in range(cols):
				line.append(0)
			self.mines.append(line)

		# Lists of coordinates
		minesRows = []
		minesCols = []

		# Create random coordinates of mines
		for i in range(numMines):
			valid = False
			while not valid:
				x = random.randint(0, rows - 1)
				y = random.randint(0, cols - 1)
				valid = True
				for i in range(len(minesRows)):
					if x == minesRows[i] and y == minesCols[i]:
						valid = False
			minesRows.append(x)
			minesCols.append(y)

		# Plot mines in "mines" matrix
		for i in range(numMines):
			x = minesRows[i]
			y = minesCols[i]
			self.mines[x][y] = MINE

		# Generate the numbers on the board, given the mines
		for x in range(rows):
			for y in range(cols):
				if not self.isMine(x, y):
					self.mines[x][y] = self.__surroundingMines(rows, cols, x, y)

	def __createHiddenMatrix(self, rows, cols):
		"""Creates a hidden matrix

		Creates a matrix indicating (with boolean values)
		which fields are closed.

		This method is not intended to be used by the client,
		it's just for internal use by other methods of this
		class."""

		self.hidden = []
		for i in range(rows):
			line = []
			for j in range(cols):
				line.append(True)
			self.hidden.append(line)

	def __surroundingMines(self, rows, cols, x, y):
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
				if (x + i >= 0 and x + i < rows) and (y + j >= 0 and y + j < cols):
					if self.isMine(x + i, y + j):
						count += 1

		return count

def main():
	test = MineBoard(4, 4, 4)

if __name__ == "__main__":
	main()