from p5 import *


class Vehicle:
    def __init__(self, start_x, start_y):
        self.pos = Vector(start_x, start_y)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.max_speed = 5
        self.max_force = 0.2
        self.size = 6

    def arrive(self, target):
        desired = target - self.pos

        if desired.magnitude < 100:
            desired.magnitude = remap(desired.magnitude, (0, 100), (0, self.max_speed))
        else:
            desired.magnitude = self.max_speed

        steering = desired - self.vel
        steering.limit(self.max_force)
        self.apply_force(steering)

    def apply_force(self, force):
        self.acc += force

    def update(self):
        self.vel += self.acc
        self.vel.limit(self.max_speed)
        self.pos += self.vel
        self.acc = Vector(0, 0)

    def display(self):
        theta = self.vel.angle + PI / 2
        fill(177)
        stroke(200)
        with push_matrix():
            translate(*self.pos)
            rotate(theta)
            triangle(
                (0, -self.size * 2),
                (-self.size, self.size * 2),
                (self.size, self.size * 2),
            )


def setup():
    global vehicle
    vehicle = Vehicle(320, 180)
    size(640, 360)
    no_stroke()


def draw():
    background(51)
    target = Vector(mouse_x, mouse_y)
    vehicle.arrive(target)
    vehicle.update()
    vehicle.display()
