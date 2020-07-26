class Light:
    def __init__(self, color):
        self.color = color


class AmbientLight(Light):
    pass


class DirectionalLight(Light):
    def __init__(self, color, direction):
        super(DirectionalLight, self).__init__(color)
        self.direction = direction


class PointLight(Light):
    def __init__(self, color, position):
        super(PointLight, self).__init__(color)
        self.position = position

