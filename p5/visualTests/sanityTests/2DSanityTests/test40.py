from random import randrange
import numpy as np
from p5 import *


class FlowField:
    def __init__(self, resolution):
        self.resolution = resolution
        self.rows = int(height / resolution)
        self.cols = int(width / resolution)
        self._field = self._generate()

    def _generate(self):
        field = []
        noise_seed(randrange(10000))
        offset = 0.1
        xoff = yoff = 0.
        for r in range(self.rows):
            field.append([])
            yoff += offset
            for _ in range(self.cols):
                # option 1
                theta = remap(noise(xoff, yoff), (0., 1.), (0., TWO_PI))
                # option 2 - fixed field
                # theta = remap(sin(xoff)+cos(yoff), (-2, 2), (0, TWO_PI))
                field[r].append(Vector(cos(theta), sin(theta)))
                xoff += offset
        return field

    def generate(self):
        self._field = self._generate()

    def lookup(self, pos):
        col = int(np.clip(pos.x // self.resolution, 0, self.cols - 1))
        row = int(np.clip(pos.y // self.resolution, 0, self.rows - 1))
        # print(row, col, self._field[row][col])
        return self._field[row][col]

    def display(self):
        for row in range(self.rows):
            for col in range(self.cols):
                pos = (col * self.resolution, row * self.resolution)
                # print(self.rows, self.cols, pos)
                self.draw_flow(self._field[row][col], pos, self.resolution - 2)

    def draw_flow(self, flow, pos, scale):
        with push_matrix():
            translate(*pos)
            stroke(200, 100)
            line((0, 0), flow * scale)


class Vehicle:
    def __init__(self, pos_x, pos_y, max_speed=4., max_force=0.1):
        self.pos = Vector(pos_x, pos_y)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.size = 4
        self.max_speed = max_speed
        self.max_force = max_force

    def follow(self, field):
        """
        Implement Reynolds's flow field following algorithm
        http://www.red3d.com/cwr/steer/FlowFollow.html
        """
        desired = field.lookup(self.pos)

        desired *= self.max_speed
        steering = desired - self.vel
        steering.limit(self.max_force)
        self.apply_force(steering)

    def apply_force(self, force):
        """
        We can use F=MA, A = Force / Mass
        """
        self.acc += force

    def update(self):
        self.vel += self.acc
        self.vel.limit(self.max_speed)
        self.pos += self.vel
        self.acc = Vector(0, 0)
        # self.acc.magnitude = 0.  # with an error, why?

    def check_borders(self):
        if self.pos.x < -self.size:
            self.pos.x = width + self.size
        if self.pos.x > width + self.size:
            self.pos.x = -self.size
        if self.pos.y < -self.size:
            self.pos.y = height + self.size
        if self.pos.y > height + self.size:
            self.pos.y = -self.size

    def display(self):
        theta = self.vel.angle + PI/2
        fill(177)
        stroke(200)
        with push_matrix():
            translate(*self.pos)
            rotate(theta)
            triangle(
                (0, -self.size * 2),
                (-self.size, self.size * 2),
                (self.size, self.size * 2)
            )

    def run(self):
        self.update()
        self.check_borders()
        self.display()


def setup():
    size(640, 360)

    global debug, flowfield, vehicles, width, height
    debug = True
    flowfield = FlowField(20)
    vehicles = [Vehicle(randrange(width), randrange(height), random_uniform(5, 20), random_uniform(0.3, 0.6))
                for _ in range(120)]


def draw():
    background(51)

    global debug, flowfield, vehicles

    if debug:
        flowfield.display()

    for v in vehicles:
        v.follow(flowfield)
        v.run()


def key_pressed():
    global debug, key
    if key == " ":
        debug = not debug


def mouse_pressed():
    global flowfield
    flowfield.generate()
