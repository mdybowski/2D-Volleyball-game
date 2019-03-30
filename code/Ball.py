import pygame
import pymunk
import pymunk.pygame_util


class Ball:
    MASS = 0.1
    MAX_VELOCITY = pymunk.Vec2d(1000.0, 1000.0)
    MAX_ANGULAR_VELOCITY = 25.0
    RADIUS = 30
    IMAGE = "res/img/ball.png"

    def __init__(self, space, pos_first_player, pos_second_player, scale_factor):
        self.mass = Ball.MASS * scale_factor['x']
        self.radius = Ball.RADIUS * scale_factor['x']
        self.max_velocity = pymunk.Vec2d(Ball.MAX_VELOCITY.x * scale_factor['x'],
                                         Ball.MAX_VELOCITY.y * scale_factor['y'])
        self.max_angular_velocity = Ball.MAX_ANGULAR_VELOCITY * scale_factor['x']

        self.start_pos_for_first_player = pymunk.Vec2d(pos_first_player)
        self.start_pos_for_second_player = pymunk.Vec2d(pos_second_player)

        moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
        self.body = pymunk.Body(self.mass, moment)
        self.body.position = pos_first_player
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.color = pygame.color.THECOLORS["black"]
        self.shape.elasticity = 0.99
        self.shape.friction = 0.8
        space.add(self.body, self.shape)

        self.attributes_to_pause = {'vel': self.body.velocity, 'ang_vel': self.body.angular_velocity,
                                    'sleeping': self.body.is_sleeping}
        self.position_to_breaks = {'pos': self.body.position, 'angle': self.body.angle}

        self.body.sleep()

    def get_start_positions(self):
        return {'player1': self.start_pos_for_first_player, 'player2': self.start_pos_for_second_player}

    def get_position(self):
        return self.body.position

    def get_position_to_breaks(self):
        return self.position_to_breaks

    def get_shape(self):
        return self.shape

    def get_radius(self):
        return self.radius

    def get_body_angle(self):
        return self.body.angle

    def is_sleeping(self):
        return self.body.is_sleeping

    def set_position(self, pos):
        self.body.position = pos

    def set_start_rotation(self):
        self.body.angle = 0.0

    def set_position_to_start_pos(self, pos):
        self.set_position(pos)

    def save_attributes_to_pause(self):
        self.attributes_to_pause['vel'] = self.body.velocity
        self.attributes_to_pause['ang_vel'] = self.body.angular_velocity
        self.attributes_to_pause['sleeping'] = self.body.is_sleeping

    def save_position(self):
        self.position_to_breaks['pos'] = self.body.position
        self.position_to_breaks['angle'] = self.body.angle

    def wakes_up(self):
        self.body.velocity = self.attributes_to_pause['vel']
        self.body.angular_velocity = self.attributes_to_pause['ang_vel']
        if self.attributes_to_pause['sleeping'] and not self.body.is_sleeping:
            self.body.sleep()

    def sleep(self):
        self.body.sleep()

    def check_velocity_restrictions(self):
        if abs(self.body.velocity.x) > self.max_velocity.x:
            self.body.velocity = pymunk.Vec2d(sign(self.body.velocity.x) * self.max_velocity.x, self.body.velocity.y)
        if abs(self.body.velocity.y) > self.max_velocity.y:
            self.body.velocity = pymunk.Vec2d(self.body.velocity.x, sign(self.body.velocity.y) * self.max_velocity.y)

        if abs(self.body.angular_velocity) > self.max_angular_velocity:
            self.body.angular_velocity = sign(self.body.angular_velocity) * self.max_angular_velocity

    def stop(self):
        self.body.velocity = pymunk.Vec2d.zero()
        self.body.angular_velocity = 0

def sign(x):
    if x > 0:
        return 1
    else:
        return -1