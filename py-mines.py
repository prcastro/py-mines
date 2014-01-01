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
	def __init__(self, rows, cols, numMines):
		# Create matrix that indicates hidden spots on the board
		self.hidden = []
		for i in range(rows):
			line = []
			for j in range(cols):
				line.append(True)
			self.hidden.append(line)

		# Initiate a matrix full of zeros that will show the mines
		# and the numbers
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
					self.mines[x][y] = self.surroundingMines(x, y)

		print(self.mines)

	def isHidden(self, x, y):
		return self.hidden[x][y]

	def isMine (self, x, y):
		if self.mines[x][y] == MINE:
			return True
		return False

	def surroundingMines(self, x, y):
	# This function considers that point (x,y) isn't a mine

	# Count the surround mines
	count = 0
	for i in range(-1, 2):
		for j in range(-1, 2):
			if self.isMine(x + i, y + j):
				count += 1

	# Return the amount of mines surrounding that point
	return count

	def drawBoard(self):
		pass

	def hasWon(self):
		for x in len(self.hidden):
			for y in len(self.hidden[0]):
				if self.hidden[x][y]:
					return False
		return True

def main():
	board = MineBoard(4,5,4)


if __name__ == "__main__":
	main()