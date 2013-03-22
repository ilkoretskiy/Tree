#!/usr/bin python
from Tkinter import *

import random

CHILD_COUNT = 4
LEFT_TOP, RIGHT_TOP, LEFT_BOTTOM, RIGHT_BOTTOM = range(CHILD_COUNT)

def get_random_point(x, y):
	tuple_point = get_random_tuple_point(x, y)
	result = Point( tuple_point )
	return result
	
def get_random_tuple_point(x, y):
	tuple_point = (random.randint(0, x), random.randint(0, y))
	return tuple_point
	
class Point(object):
	def __init__(self, *args, **kwargs):
		if len(args) == 1:
			if not type(args[0]) is tuple:
				raise Exception("val must be tuple, not %s" % (str(type(args[0]))))
			self.assign(*args[0])
		else:
			self.assign(args[0], args[1])
		
	def assign(self, x, y):
		self.x, self.y = x, y
		
	def __str__(self):
		return "x(%d) y(%d)" % (self.x, self.y)

class Rect(object):
	def __init__(self, x, y, width, height):
		# !!TODO remeber, now width and height used as bottom and right coord
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		
	def __str__(self):
		return "rect x1(%d) y1(%d) x2(%d) y2(%d)" % (self.x, self.y, self.width, self.height)

class Node(object):
	def __init__(self, capacity, rect, parent = None):	
		self.__coord = Point((rect.x + rect.width) / 2, (rect.y + rect.height) / 2)
		#print "coord", self.__coord
		self.__rect = rect
		self.__capacity = capacity
		self.__children = []
		self.__points = []
		self.parent = parent

	def has_children(self):
		return len(self.__children)  != 0
		
	def is_empty(self):
		return len(self.__points) == 0 and not self.has_children()
	
	def ready_for_points(self):
		# if there are a place for new points and haven't children yet
		return len(self.__points) <= self.__capacity and not self.has_children()

	def get_coord(self):
		return self.__coord
	
	def get_rect(self):
		return self.__rect
		
	def get_children(self):
		return self.__children
		
	def get_points(self):
		return self.__points
	

	def get_node_for_point(self, point):
		if type(point) != Point:
			point = Point(point)
		child = None
		#print "compare" , point, self.__coord
		if point.x < self.__coord.x:
			if point.y < self.__coord.y:
				#print "LEFT_TOP"
				child = self.__children[LEFT_TOP]
			else:
				#print "LEFT_BOTTOM"
				child = self.__children[LEFT_BOTTOM]
		else:
			if point.y < self.__coord.y:
				#print "RIGHT_TOP"
				child = self.__children[RIGHT_TOP]
			else:
				#print "RIGHT_BOTTOM"
				child = self.__children[RIGHT_BOTTOM]
		return child
	
	def add_point(self, point):
		if type(point) != Point:
			point = Point(point)
		self.__points.append(point)
		if self.__need_to_split() and self.__can_split():
			self.__split_node()
		
		if not self.__can_split():
			print "can't split"
			
	def __need_to_split(self):
		return len(self.__points) > self.__capacity
		
	def __can_split(self):
		return abs(self.__rect.width - self.__rect.x) > 1 and abs(self.__rect.height - self.__rect.y)
	
	def __split_rect_by_index(self, rect, idx):
		output_rect = None
		if idx == LEFT_TOP:
			output_rect = Rect(rect.x, rect.y, (rect.x + rect.width) / 2, (rect.y + rect.height) / 2)
		elif idx == RIGHT_TOP:
			output_rect = Rect((rect.x + rect.width) / 2, rect.y, rect.width, (rect.y + rect.height) / 2)
		elif idx == LEFT_BOTTOM:
			output_rect = Rect(rect.x, (rect.y + rect.height) / 2, (rect.x + rect.width) / 2, rect.height)
		elif idx == RIGHT_BOTTOM:
			output_rect = Rect((rect.x + rect.width) / 2, (rect.y + rect.height) / 2, rect.width, rect.height)		
		#print output_rect
		return output_rect
	
	def __split_node(self):
		# create children
		#print "<child creation>"
		#print "splitted rect", self.__rect
		self.__children = [Node(self.__capacity, self.__split_rect_by_index(self.__rect, i), self) for i in range(CHILD_COUNT)]
		#print "<\child creation>"
		# rearrange points to children
		for point in self.__points:			
			child = self.get_node_for_point(point)			
			child.add_point(point)
		# erase points lise of current node
		self.__points = []
			
	def __str__(self):
		return "Node point_count(%s/%s)" % (len(self.__points), self.__capacity)
			
class Tree(object):
	def __init__(self, rect, node_capacity):
		self.__node_capacity = node_capacity
		self.__root = Node(self.__node_capacity, rect)
		self.__canvas = None		

	def insert(self, point):
		if type(point) != Point:
			point = Point(point)
		node = self.__root
		parent = node	
		while (1):
			#print 'current point', point
			if node.ready_for_points():
				node.add_point(point)
				break
			else:
				parent = node
				node = node.get_node_for_point(point)
		self.redraw()
		
	def set_canvas(self, canvas):
		self.__canvas = canvas
		self.redraw()
	
	def redraw(self):
		if self.__canvas == None:
			return
		self.__recursive_drawing(self.__root)

	
	def __recursive_drawing(self, node):		
		coord = node.get_coord()		
		rect = node.get_rect()

		self.__canvas.create_rectangle(rect.x + 1, rect.y + 1, rect.width - 1, rect.height - 1)
				
		if node.is_empty():
			return
		
		rad = 2
		points = node.get_points()
		for point in points:
				self.__canvas.create_oval(point.x - rad, point.y - rad, point.x + rad, point.y + rad, fill = 'red')
		
		children = node.get_children()		
		for child in children:
			self.__recursive_drawing(child)

canvas_size = {'width' : 800, 'height' : 800}
canvas_rect = Rect(0, 0, canvas_size['width'], canvas_size['height'])
point_per_node = 1
tree = Tree(canvas_rect, node_capacity = point_per_node)

def callback(event):
	point = (event.x, event.y)
	tree.insert(point)

def get_canvas():
	root = Tk()
	canvas = Canvas(root, **canvas_size)
	canvas.pack()
	canvas.bind("<Button-1>", callback)	
	return canvas

def main():
	canvas = get_canvas()	
	tree.set_canvas(canvas)	
	mainloop()

if __name__ == "__main__":
	main()
