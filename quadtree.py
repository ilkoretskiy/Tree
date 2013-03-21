#!/usr/bin python
from Tkinter import *

VERTICAL, HORIZONTAL = xrange(2)

class Point(object):
	def __init__(self, tuple_point):
		if not type(tuple_point) is tuple:
			raise Exception("val must be tuple")
		self.x, self.y = tuple_point		

class Node(object):
	def __init__(self):
		self.val = None
		#self.points

	def isEmpty(self):
		return self.val == None

	def init(self, val):
		if self.val != None:
			raise Exception("val already exist")
		else:
			self.val = Point(val)
		self.left_bottom = Node()
		self.left_top = Node()
		self.right_bottom = Node()
		self.right_top = Node()

	def get_val(self):
		return self.val
	
	def set_orientation(self, orientation):
		self.__orientation = orientation
	
	def get_orientation(self):
		return self.__orientation
		
	def __lt__(self, val):	
		if type(val) != tuple:			
			raise Exception("can compare only with tuple")
		
		if self.__orientation == VERTICAL:
			return self.val.x < val[0]
		else:
			return self.val.y < val[1]
	
	def __gt__(self, val):
		if type(val) != tuple:			
			raise Exception("can compare only with tuple")
		
		if self.__orientation == VERTICAL:
			return self.val.x > val[0]
		else:
			return self.val.y > val[1]
			
	def __str__(self):
		return "Node %s %s" % ("isEmpty" if self.isEmpty() else "filled", "Vertical" if self.__orientation == 0 else "Horizontal")
			
class Tree(object):
	def __init__(self):
		self.__root = Node()
		self.__canvas = None
		self.__node_capacity = 1

	def insert(self, point):
		node = self.__root
		parent = node
		
		while (1):
			if node.isFull():
			else:
				node.add_point(Point(point))
		
		"""
		parent = node
		while 1:
			#print node
			if node.isEmpty():
				node.init(point)
				break
			else:
				parent = node
				if node < point:
					node = node.right
				else:
					node = node.left									

		self.redraw()
		"""
		
	def set_canvas(self, canvas):
		self.__canvas = canvas
		self.redraw()
	
	def redraw(self):
		if self.__canvas == None:
			return
			#raise Exception("canvas is null")
		width = self.__canvas.cget('width')
		height = self.__canvas.cget('height')
		rect = (0, 0, width, height)
		self.__recursive_drawing(self.__root, rect)
	
	def __split_rect(self, node, rect):
		point = node.get_val()
		orientation = node.get_orientation()
		left_rect = ()
		right_rect = ()

		if orientation == VERTICAL:
			left_rect = (rect[0], rect[1], point.x, rect[3])
			right_rect= (point.x, rect[1], rect[2], rect[3])
			#self.__canvas.create_line(point.x, rect[1], point.x, rect[3])
		else:
			left_rect  = (rect[0], rect[1], rect[2], point.y)
			right_rect = (rect[0], point.y, rect[2], rect[3])
				
		return left_rect, right_rect
		
	
	def __recursive_drawing(self, node, rect):
		point = node.get_val()
		orientation = node.get_orientation()
		rad = 2
		self.__canvas.create_oval(point.x - rad, point.y - rad, point.x + rad, point.y + rad, fill = 'red')
		if orientation == VERTICAL:
			self.__canvas.create_line(point.x, rect[1], point.x, rect[3])
		else:
			self.__canvas.create_line(rect[0], point.y, rect[2], point.y)
			
		left_rect, right_rect = self.__split_rect(node, rect)
		
		if not node.left.isEmpty():
			self.__recursive_drawing(node.left, left_rect)
		if not node.right.isEmpty():
			self.__recursive_drawing(node.right, right_rect)

canvas_size = {'width' : 400, 'height' : 400}
tree = Tree()

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
	tree.insert((canvas_size['width'] / 2, canvas_size['height'] / 2))	
	tree.set_canvas(canvas)	
	mainloop()

if __name__ == "__main__":
	main()
