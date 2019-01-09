import numpy as np
import tkinter
import csv
from ast import literal_eval

class Point():
	"""Object holding the probability to move to the neighbors 
		of a gridpoint"""
	def __init__(self, p_up, p_down, p_left, p_right, p_self, co):
		self.p_up = p_up
		self.p_down = p_down
		self.p_left = p_left
		self.p_right = p_right
		self.p_self = p_self

		# neighboring points in grid initialised as none
		self.n_up = None
		self.n_down = None
		self.n_left = None
		self.n_right = None
		
		self.tracer = 0
		self.new_tracer = 0

		self.co = co

	def move_up(self):
		return self.p_up * self.tracer
	
	def move_down(self):
		return self.p_down * self.tracer
	
	def move_left(self):
		return self.p_left * self.tracer
		
	def move_right(self):
		return self.p_right * self.tracer

	def move_self(self):
		return self.p_self * self.tracer

class Model():
	"""
		Array dat point objecten bevat
	"""
	def __init__(self, height, width):
		self.height = height
		self.width = width
		self.grid = np.empty((height, width), dtype=object)
		self.filename = 'temp.csv'
		
		# initialise array with point objects without probabilitys
		for i in range(self.height):
			for j in range(self.width):
				self.grid[i][j] = Point(0,0,0,0,0,(i,j))
		
		# Set the neighbors of all the points in the grid
		for i in range(self.height):
			for j in range(self.width):
				point = self.grid[i][j]
				#print(self.grid[i-1][j])
				point.n_up = self.grid[i-1][j]
				try:
					point.n_down = self.grid[i+1][j]
				except:
					pass
				point.n_left = self.grid[i][j-1]
				try:
					point.n_right = self.grid[i][j+1]
				except:
					pass

				# exceptions for when np array wraps around
				if i == 0:
					point.n_up = None
				if i == height - 1:
					point.n_down = None
				if j == 0:
					point.n_left = None
				if j == width - 1:
					point.n_right = None

	# Loop over the grid and advances every point to the next step
	# by finding the neighbors and passing the right ammount of tracer to them
	def update(self):
		for x in range(self.height):
			for y in range(self.width):
				point = self.grid[x][y]
				if point.n_up is not None:
					point.n_up.new_tracer += point.move_up()
				if point.n_down is not None:
					point.n_down.new_tracer += point.move_down()
				if point.n_left is not None:
					point.n_left.new_tracer += point.move_left()
				if point.n_right is not None:
					point.n_right.new_tracer += point.move_right()
				point.new_tracer += point.move_self()
		
		# Set the incoming tracer as the current tracer
		for x in range(self.height):
			for y in range(self.width):
				point = self.grid[x][y]
				point.tracer = point.new_tracer
				point.new_tracer = 0

	# Set tracer of a single point
	def set_tracer(self, xco, yco, tracer):
		self.grid[xco][yco].tracer = tracer

	# Sets chances of a point to given parameters 
	def set_chances(self, xco, yco, up, down, right, left, self_):
		point = self.grid[xco][yco]
		point.p_up = up
		point.p_down = down
		point.p_right = right
		point.p_left = left
		point.p_self = self_

	# print entire grid tracer amount per point
	def print(self):
		printgrid = np.empty((self.height, self.width))
		for x in range(self.height):
			for y in range(self.width):
				printgrid[x][y] = self.grid[x][y].tracer
		print(printgrid)

	# Save the transition states to a csv
	def save_transition_chances(self):
		with open(self.filename, 'w') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			for x in range(self.height):
				for y in range(self.width):
					point = self.grid[x][y]
					writer.writerow([(x, y), point.p_up, point.p_down,
											point.p_right, point.p_left, 
											point.p_self])

	# Read in transition states to grid in model
	def read_transition_states(self, filename):
		with open(filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				x, y = literal_eval(row[0])
				self.grid[x][y].p_up = row[1]
				self.grid[x][y].p_down = row[2]
				self.grid[x][y].p_right = row[3]
				self.grid[x][y].p_left = row[4]
				self.grid[x][y].p_self = row[5]
