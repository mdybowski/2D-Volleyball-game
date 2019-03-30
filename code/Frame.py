import pymunk
import pymunk.pygame_util


class Frame:

    def __init__(self, space, pos1, pos2, width):
        self.position1 = pymunk.Vec2d(pos1)
        self.position2 = pymunk.Vec2d(pos2)
        self.width = width
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, pos1, pos2, width)
        space.add(self.shape)

    def get_shape(self):
        return self.shape

    def get_positions(self):
        return self.position1, self.position2


class Ground(Frame):

    def __init__(self, space, pos1, pos2, width):
        super(Ground, self).__init__(space, pos1, pos2, width)


class Wall(Frame):

    def __init__(self, space, pos1, pos2, width):
        super(Wall, self).__init__(space, pos1, pos2, width)
        self.shape.elasticity = 0.99
        self.shape.friction = 0.99


class Net(Frame):
    NET_COLOR = (150, 80, 0)
    THICKNESS = 5

    def __init__(self, space, pos1, pos2, width):
        super(Net, self).__init__(space, pos1, pos2, width)
        self.shape.elasticity = 0.99
        self.shape.friction = 0.99
        self.shape.color = Net.NET_COLOR