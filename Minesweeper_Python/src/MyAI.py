# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action


class MyAI( AI ):
	dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		self.uncovered = set()
		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.coveredTiles = rowDimension * colDimension
		self.totalMines = totalMines
		# -2 marked, -1 unmarked
		self.board = [[-1] * rowDimension for _ in range(colDimension)]
		self.prev_tile = None
		self.safe_spots = [(startX, startY)]
		
	def getAction(self, number: int):
		
		if self.coveredTiles <= self.totalMines:
			return Action(AI.Action.LEAVE)
		
		if self.prev_tile:
			prevX, prevY = self.prev_tile
			self.board[prevX][prevY] = number
			numNeighbors, numMarked = self.getMarkedNeighbors(prevX, prevY)
			effectiveLabel = number - numMarked

			if number == numNeighbors:
				self.markNeighbors(prevX, prevY)
			elif effectiveLabel == 0:
				self.safeNeighbors(prevX, prevY, self.safe_spots)

		if not self.safe_spots:
			spots = self.unCoverAllExceptCenter()
			for pair in spots:
				self.safe_spots.append(pair)
		if self.safe_spots:
			nextX, nextY = self.safe_spots.pop()
			self.coveredTiles -= 1
			self.prev_tile = (nextX, nextY)
			return Action(AI.Action.UNCOVER, nextX, nextY)
			
		
		return Action(AI.Action.LEAVE)
		
	def getMarkedNeighbors(self, x, y):
		neighbors = 0
		marked = 0
		for dx, dy in self.dirs:
			nx, ny = x + dx, y + dy
			if 0 <= nx < self.colDimension and 0 <= ny < self.rowDimension:
				neighbors += 1
				if self.board[nx][ny] == -2:
					marked += 1
		return (neighbors, marked)
	
	def markNeighbors(self, x, y):
		for dx, dy in self.dirs:
			nx, ny = x + dx, y + dy
			if 0 <= nx < self.colDimension and 0 <= ny < self.rowDimension:
				self.board[nx][ny] = -2

	def safeNeighbors(self, x, y, q):
		for dx, dy in self.dirs:
				nx, ny = x + dx, y + dy
				if 0 <= nx < self.colDimension and 0 <= ny < self.rowDimension:
					if self.board[nx][ny] == -1 and (nx, ny) not in self.uncovered:
						self.uncovered.add((nx, ny))
						q.append((nx, ny))
    
	def unCoverAllExceptCenter(self):
		center_x = self.colDimension // 2
		center_y = self.rowDimension // 2
		mindist = float('inf')
		for x in range(self.colDimension):
			for y in range(self.rowDimension):
				if self.board[x][y] == -1:
					mindist = min(mindist, abs(x-center_x) + abs(y-center_y))
		
		q = []
		for x in range(self.colDimension):
			for y in range(self.rowDimension):
				if self.board[x][y] == -1 and abs(x-center_x) + abs(y-center_y) > mindist:
					q.append((x, y))
		return q