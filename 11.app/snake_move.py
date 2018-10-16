# coding: utf-8

from queue import PriorityQueue

from display import BpiBitNeoPixel, NeoPixelPower

from random import randint
import time

NeoPixelPower(True)

class SnakeMap(object):
	
	def __init__(self):
		self.View = BpiBitNeoPixel()
		# Snake 1 Food 2 None 0 In Area
		self.Area = [0] * self.View.Sum
		self.Snake = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0]
		self.Area[0], self.Area[1] = 1, 0
	
	def Move(self, pos):
		x, y = pos % self.View.Max, pos / self.View.Max
		# Check Move Next
		next = pos - 1
		if x >= (self.View.Min + 1) and self.Area[next] != 1:
			self.Area[next] = 1
			return next # Left
		next = pos + 1
		if x < (self.View.Max - 1) and self.Area[next] != 1:
			self.Area[next] = 1
			return next # Right
		next = pos - self.View.Max
		if y >= (self.View.Min + 1) and self.Area[next] != 1:
			self.Area[next] = 1
			return next # Up
		next = pos + self.View.Max
		if y < (self.View.Max - 1) and self.Area[next] != 1:
			self.Area[next] = 1
			return next # Down
		return None
		
	def Find(self):
		pass
		
	def Run(self):
		# Move Snake
		result = self.Move(self.Snake[len(self.Snake) - 1])
		if(None != result):
			self.Snake.append(result)
			# Load Snake Body
			for Pos in range(len(self.Snake)):
				self.View.LoadP(self.Snake[Pos], (0, 0, (Pos + 1)))
			# Clear Snake Tail
			self.View.LoadP(self.Snake[0], (0, 0, 0))
			self.Area[self.Snake[0]] = 0
			self.Snake.pop(0)
		# Show Snake
		self.View.Show()
		time.sleep(0.1)
		return (None != result);
	
Test = SnakeMap()
for i in range(50):
	if(False == Test.Run()):
		break
