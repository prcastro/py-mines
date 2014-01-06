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

		self.rows = rows
		self.cols = cols

		self.__createBoardMatrix(numMines)
		self.__createHiddenMatrix()

		print(self.board)

	def openField(self, x, y):
		"""Open a field on the board"""

		if self.isMine(x, y):
			self.__gameLost()
		else:
			self.hidden[x][y] = False
			if self.board[x][y] == 0:
				self.__openSurroundingFields(x, y)

	def hasLost(self):
		"""Check if the player lost the game.

		This method may be deleted if not useful. This
		will depend on the game implementation"""
		for mine in self.mines:
			x, y = mine
			if not isHidden(x, y):
				return True

		return False

	def hasWon(self):
		"""Check if the player won the game."""

		for x in len(self.hidden):
			for y in len(self.hidden[0]):
				if isHidden(x, y) and not isMine(x, y):
					return False
		return True

	def isHidden(self, x, y):
		"""Check if the field at the (x,y) coordinate is hidden.

		Returns True if it's hidden and False otherwise."""

		return self.hidden[x][y]

	def isMine (self, x, y):
		"""Check if the field at the (x,y) coordinate is a mine.

		Returns True if it's a mine and False otherwise."""

		return self.board[x][y] == MINE

	def __createBoardMatrix(self, numMines):
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

		self.board = []
		for i in range(self.rows):
			line = []
			for j in range(self.cols):
				line.append(0)
			self.board.append(line)

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

		# Plot mines in "board" matrix and make mines list
		self.mines = []
		for i in range(numMines):
			x, y = minesRows[i], minesCols[i]
			self.board[x][y] = MINE
			self.mines.append((x, y))

		# Generate the numbers on the board, given the mines
		for x in range(self.rows):
			for y in range(self.cols):
				if not self.isMine(x, y):
					self.board[x][y] = self.__surroundingMines(x, y)

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
	test = MineBoard(4, 4, 4)

if __name__ == "__main__":
	main()