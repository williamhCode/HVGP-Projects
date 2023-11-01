from pygame.math import Vector2
from .polygon import Polygon

gravity = 2500/60
class Bird(Polygon):

    def __init__(self, width, height, pos: Vector2, vel:Vector2=0, ang=0):
        self.width = width
        self.height = height
        orig_points = (Vector2(-width * 0.5, height * 0.2), Vector2(-width * 0.3, height * 0.5), Vector2(width * 0.45, height * 0.5), Vector2(width * 0.45, -height * 0.1), Vector2(width * 0.2, -height * 0.5), Vector2(-width * 0.2, -height * 0.5), Vector2(-width * 0.5, -height * 0.1))
        super().__init__(orig_points, pos, vel, ang)
        self.mode = 0
        self.frame = 0
        self.frame_time = 0
        self.flap_time = 4

        self.rising = False

    def update_motion(self):
        if self.frame_time >= self.flap_time:
            self.frame_time = 0
            if self.frame >= 3:
                self.frame = 0
            elif self.ang > 50 and self.frame == 1:
                pass
            else:
                self.frame += 1
        else:
            self.frame_time += 1
    
    def update(self):
        if self.rising:
            if self.ang -18 < -20:
                self.rising = False
                self.ang = -18
            else:
                self.ang -= 20
        elif self.vel.y > 650 and self.ang < 90:
            self.ang += 6
        elif self.ang >= 90:
            self.ang == 90
            self.vel.y = 850
        super().update()
        if self.vel.y < 650:
            self.vel.y += gravity

    def set_start(self):
        self.mode = 1
        self.frame = 3

    def jump(self):
        self.frame = 0
        self.frame_time = 0

        self.vel.y = -700
        self.rising = True
        
    def get_img_frame(self):
        return self.frame
