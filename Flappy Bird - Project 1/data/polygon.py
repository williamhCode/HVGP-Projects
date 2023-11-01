from pygame.math import Vector2
import math

class Polygon:

	def __init__(self, orig_points, pos: Vector2, vel: Vector2, ang):
		self.orig_points = orig_points
		self.pos = pos
		self.vel = vel
		self.ang = ang
		self.calc_points()

	def update(self):
		self.pos += self.vel / 60
		self.calc_points()

	def calc_points(self):
		self.points = tuple(Vector2(*transform_vector(point, self.pos, self.ang)) for point in self.orig_points)

def transform_vector(point: Vector2, pos: Vector2, degrees):
	x, y = point.x, point.y
	radians = math.radians(degrees)

	xx = x * math.cos(radians) - y * math.sin(radians) + pos.x
	yy = x * math.sin(radians) + y * math.cos(radians) + pos.y

	return xx, yy

def overlap_SAT(polygon1: Polygon, polygon2: Polygon):
	poly1 = polygon1
	poly2 = polygon2

	for shape in range(2):
		if shape == 1:
			poly1 = polygon2
			poly2 = polygon1

		for a in range(len(poly1.points)):
			b = (a+1) % len(poly1.points)
			axisProj = Vector2(-(poly1.points[b].y - poly1.points[a].y), poly1.points[b].x - poly1.points[a].x)

			min_r1, max_r1 = math.inf, -math.inf
			for point in poly1.points:
				q = point.dot(axisProj)
				min_r1 = min(min_r1, q)
				max_r1 = max(max_r1, q)

			min_r2, max_r2 = math.inf, -math.inf
			for point in poly2.points:
				q = point.dot(axisProj)
				min_r2 = min(min_r2, q)
				max_r2 = max(max_r2, q)

			if not(max_r2 >= min_r1 and max_r1 >= min_r2):
				return False

	return True