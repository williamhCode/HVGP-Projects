from .polygon import Polygon
from pygame.math import Vector2
from copy import copy

class Pipes:

    def __init__(self, width, height, xpos, yoffset):
        pos = Vector2(xpos, 300 + yoffset)
        vel = Vector2(-240, 0)

        pipes_gap = 210
        top_points = (Vector2(-width/2, -pipes_gap/2), Vector2(width/2, -pipes_gap/2), Vector2(width/2, -pipes_gap/2 - height), Vector2(-width/2, -pipes_gap/2 - height))
        self.top_pipe = Polygon(top_points, pos, vel, 0)

        bottom_points = (Vector2(-width/2, pipes_gap/2), Vector2(width/2, pipes_gap/2), Vector2(width/2, pipes_gap/2 + height), Vector2(-width/2, pipes_gap/2 + height))
        self.bottom_pipe = Polygon(bottom_points, copy(pos), copy(vel), 0)

    def update(self):
        self.top_pipe.update()
        self.bottom_pipe.update()