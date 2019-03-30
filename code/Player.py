import pygame
import pymunk
import pymunk.pygame_util


class Player:
    MASS = 100
    VELOCITY = 400.0
    JUMP_VELOCITY = 800.0
    RADIUS = 40
    IMAGE = {'player1': "res/img/player1.png", 'player2': "res/img/player2.png"}

    def __init__(self, space, pos, scale_factor):
        self.mass = Player.MASS * scale_factor['x']
        self.radius = Player.RADIUS * scale_factor['x']
        self.jump_velocity = Player.JUMP_VELOCITY * scale_factor['y']
        self.speed = Player.VELOCITY * scale_factor['x']

        self.start_pos = pymunk.Vec2d(pos)
        self.jumping = False
        self.block_move = {'left': False, 'right': False}
        self.won = False
        self.serves = True
        self.dominates = False
        self.collides_with_ball = False
        self.bounce_counter = 0
        self.score = 0

        moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
        self.body = pymunk.Body(self.mass, moment)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.color = pygame.color.THECOLORS["black"]
        self.shape.elasticity = 0.99
        self.shape.friction = 0.4
        space.add(self.body, self.shape)

        self.attribute_to_pause = self.body.velocity.y
        self.position_to_breaks = self.body.position

    def get_position(self):
        return self.body.position

    def get_radius(self):
        return self.radius

    def get_block_move(self):
        return self.block_move

    def get_start_position(self):
        return self.start_pos

    def get_shape(self):
        return self.shape

    def get_score(self):
        return self.score

    def get_position_to_breaks(self):
        return self.position_to_breaks

    def check_bounce_counter(self):
        if self.serves:
            return self.bounce_counter > 1
        else:
            return self.bounce_counter > 3

    def check_if_won(self):
        return self.score >= 21 and self.dominates

    def is_jumping(self):
        return self.jumping

    def is_falling(self):
        return self.jumping and self.body.velocity.y <= 0.0

    def is_sleeping(self):
        return self.body.is_sleeping

    def collision_with_ball(self):
        return self.collides_with_ball

    def set_dominance(self, dominance):
        self.dominates = dominance

    def set_serving(self, serving):
        self.serves = serving

    def set_collision_with_ball(self, collides):
        self.collides_with_ball = collides

    def set_block_move(self, is_blocked, direction):
        self.block_move[direction] = is_blocked

    def set_position_to_start_pos(self):
        self.body.position = self.start_pos

    def set_jumping(self, is_jumping):
        self.jumping = is_jumping

    def set_position(self, pos):
        self.body.position = pos

    def set_start_rotation(self):
        self.body.angle = 0.0
        self.body.angular_velocity = 0.0

    def reset_bounce_counter(self):
        self.bounce_counter = 0

    def increment_bounce_counter(self):
        self.bounce_counter += 1

    def is_winner(self):
        self.won = True

    def clear_score(self):
        self.won = False
        self.score = 0

    def jump(self):
        self.body.velocity = pymunk.Vec2d(0.0, self.jump_velocity)
        self.jumping = True

    def moves(self, direction):
        self.body.velocity = pymunk.Vec2d(direction * self.speed, self.body.velocity.y)

    def stop(self):
        self.body.velocity = pymunk.Vec2d(0.0, self.body.velocity.y)

    def definitive_stop(self):
        self.body.velocity = pymunk.Vec2d.zero()

    def wakes_up(self):
        self.body.velocity = pymunk.Vec2d(0.0, self.attribute_to_pause)

    def sleep(self):
        self.body.sleep()

    def save_attribute_to_pause(self):
        self.attribute_to_pause = self.body.velocity.y

    def save_position(self):
        self.position_to_breaks = self.body.position

    def gained_point(self):
        self.score += 1