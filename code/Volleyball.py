import sys
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
import math


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
        self.shape.color = pygame.color.THECOLORS["white"]
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


class Text:
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    SIZE = 100
    MAIN_FONT = "res/fonts/BKANT.ttf"

    def __init__(self, font_source, scale_factor, text_color, text, text_pos_x=0, text_pos_y=0):
        main_font = pygame.font.Font(font_source, int(Text.SIZE * scale_factor))
        self.text_surf = main_font.render(text, True, text_color)
        self.text_size = pymunk.Vec2d(self.text_surf.get_width(), self.text_surf.get_height())
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = (text_pos_x, text_pos_y)

    def to_draw(self):
        return self.text_surf, self.text_rect

    def set_text_center(self, text_pos):
        self.text_rect.center = text_pos


class Game:

    CAPTION = 'Volleyball'
    GRAVITY = (0.0, -900.0)
    BACKGROUND = "res/img/background.png"
    MAIN_MUSIC = "res/sounds/main_music.mp3"
    BOUNCE_SOUND = "res/sounds/Bounce.wav"
    JUMP_SOUND = "res/sounds/Jump.wav"
    SETTINGS = "res/Settings.txt"
    STEP_WORLD = 1/50.0
    gained_point = {'player1': False, 'player2': False}
    break_timer = 0

    def __init__(self, window_size, fps):
        window = pymunk.Vec2d(window_size)

        self.window = window
        self.FPS = fps

        self.paused = False
        self.waiting = False

        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()

        pygame.mixer.music.load(Game.MAIN_MUSIC)
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

        self.bounce_ball_sound = pygame.mixer.Sound(Game.BOUNCE_SOUND)
        self.jump_sound = pygame.mixer.Sound(Game.JUMP_SOUND)

        self.fpsClock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(Game.CAPTION)

        scale_factor_x_y = pymunk.Vec2d(window.x / 1200, window.y / 650)
        self.scale_factor = {'x': scale_factor_x_y.x, 'y': scale_factor_x_y.y,
                             'xy': min(scale_factor_x_y.x, scale_factor_x_y.y)}
        self.gravity = (0.0, Game.GRAVITY[1] * self.scale_factor['y'])

        self.space = self.create_space(self.gravity)

        players_radius = Player.RADIUS * self.scale_factor['x']

        start_pos_first_player = (window.x - window.x / 24 - players_radius, window.y / 22 + players_radius)
        start_pos_second_player = (players_radius + window.x / 24, window.y / 22 + players_radius)

        start_ball_pos_for_first_player = (3 * window.x / 4 - window.x / 12, window.y / 2 + window.y / 13)
        start_ball_pos_for_second_player = (window.x / 4 + window.x / 12, window.y / 2 + window.y / 13)

        self.player1 = Player(self.space, start_pos_first_player, self.scale_factor)
        self.player2 = Player(self.space, start_pos_second_player, self.scale_factor)

        self.ball = Ball(self.space, start_ball_pos_for_first_player, start_ball_pos_for_second_player,
                         self.scale_factor)

        self.frames = self.create_frames(self.space, window, self.scale_factor)
        self.game_texts = self.create_texts(window, self.scale_factor)

        self.background = self.load_image(window_size, self.BACKGROUND, True)
        self.ball_image = self.load_image((int(2 * self.ball.get_radius()),
                                           int(2 * self.ball.get_radius())), Ball.IMAGE, False)
        self.player1_image = self.load_image((int(2 * self.player1.get_radius()),
                                              int(2 * self.player1.get_radius())), Player.IMAGE['player1'], False)
        self.player2_image = self.load_image((int(2 * self.player2.get_radius()),
                                              int(2 * self.player2.get_radius())), Player.IMAGE['player2'], False)

        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES

    def pause(self):
        self.paused = True
        self.ball.save_attributes_to_pause()
        self.player1.save_attribute_to_pause()
        self.player2.save_attribute_to_pause()
        if not self.ball.is_sleeping():
            self.ball.sleep()
        if not self.player1.is_sleeping():
            self.player1.sleep()
        if not self.player2.is_sleeping():
            self.player2.sleep()

    def resume(self):
        self.paused = False
        self.ball.wakes_up()
        self.player1.wakes_up()
        self.player2.wakes_up()

    def restart(self):
        self.paused = False
        self.game_texts['winner_text'] = None
        self.player1.clear_score()
        self.player2.clear_score()
        self.game_texts['general_score_text'] = Text(Text.MAIN_FONT, self.scale_factor['xy'], Text.BLACK, '0:0',
                                                     self.window.x / 2, 0.25 * self.window.y)

    def is_paused(self):
        return self.paused

    def wait(self, waiting):
        self.waiting = waiting

    def is_waiting(self):
        return self.waiting

    def check_if_someone_won(self):
        if self.player1.check_if_won():
            self.player1.is_winner()
            self.pause()
            self.game_texts['winner_text'] = Text(Text.MAIN_FONT, 1.3 * self.scale_factor['xy'], Text.RED,
                                                  'PLAYER 1 WON', self.window.x / 2, self.window.y / 2)
        elif self.player2.check_if_won():
            self.player2.is_winner()
            self.pause()
            self.game_texts['winner_text'] = Text(Text.MAIN_FONT, 1.3 * self.scale_factor['xy'], Text.RED,
                                                  'PLAYER 2 WON', self.window.x / 2, self.window.y / 2)

    def end_game(self):
        return self.game_texts['winner_text']

    def update_general_score_text(self):
        self.game_texts['general_score_text'] = Text(Text.MAIN_FONT, self.scale_factor['xy'],
                                                     Text.BLACK, '{}:{}'.format(self.player2.get_score(),
                                                                                self.player1.get_score()),
                                                     self.window.x / 2, 0.25 * self.window.y)

    def update_player1(self, list_of_events):
        for event in list_of_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not self.player1.is_jumping():
                    self.player1.jump()
                    pygame.mixer.Sound.play(self.jump_sound)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player1.stop()

        if self.player1.get_position().y <= self.player1.get_start_position().y + 20 * self.scale_factor['y'] and\
                self.player1.is_falling():
            self.player1.set_jumping(False)
            self.player1.definitive_stop()
            self.player1.set_position((self.player1.get_position().x, self.player1.get_start_position().y))

        if self.player1.get_position().x - self.player1.get_radius() <=\
                self.frames['net'].get_positions()[0].x + 0.3 * self.player1.get_radius():
            self.player1.set_block_move(True, 'left')
        else:
            self.player1.set_block_move(False, 'left')
        if self.player1.get_position().x >= self.window.x - 1.3 * self.player1.get_radius():
            self.player1.set_block_move(True, 'right')
        else:
            self.player1.set_block_move(False, 'right')

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_RIGHT]:
            if self.player1.get_block_move()['right']:
                self.player1.stop()
                self.player1.set_position((self.window.x - self.player1.get_radius(), self.player1.get_position().y))
            else:
                self.player1.moves(1)
        if keys_pressed[K_LEFT]:
            if self.player1.get_block_move()['left']:
                self.player1.stop()
                self.player1.set_position((self.frames['net'].get_positions()[0].x + 1.3 * self.player1.get_radius(),
                                           self.player1.get_position().y))
            else:
                self.player1.moves(-1)
        if keys_pressed[K_RIGHT] and keys_pressed[K_LEFT]:
            self.player1.stop()

    def update_player2(self, list_of_events):
        for event in list_of_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not self.player2.is_jumping():
                    self.player2.jump()
                    pygame.mixer.Sound.play(self.jump_sound)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    self.player2.stop()

        if self.player2.get_position().y <= self.player2.get_start_position().y + 20 * self.scale_factor['y'] and\
                self.player2.is_falling():
            self.player2.set_jumping(False)
            self.player2.definitive_stop()
            self.player2.set_position((self.player2.get_position().x, self.player2.get_start_position().y))

        if self.player2.get_position().x + self.player2.get_radius() >= \
                self.frames['net'].get_positions()[0].x - 0.3 * self.player2.get_radius():
            self.player2.set_block_move(True, 'right')
        else:
            self.player2.set_block_move(False, 'right')
        if self.player2.get_position().x <= 1.3 * self.player2.get_radius():
            self.player2.set_block_move(True, 'left')
        else:
            self.player2.set_block_move(False, 'left')

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_d]:
            if self.player2.get_block_move()['right']:
                self.player2.stop()
                self.player2.set_position((self.frames['net'].get_positions()[0].x - 1.3 * self.player2.get_radius(),
                                           self.player2.get_position().y))
            else:
                self.player2.moves(1)
        if keys_pressed[K_a]:
            if self.player2.get_block_move()['left']:
                self.player2.stop()
                self.player2.set_position((self.player2.get_radius(), self.player2.get_position().y))
            else:
                self.player2.moves(-1)
        if keys_pressed[K_a] and keys_pressed[K_d]:
            self.player2.stop()

    def check_if_ball_collides_with_sth(self):
        if self.check_collision(self.player2, self.ball):
            self.player2.set_start_rotation()
            if not self.player2.collision_with_ball():
                self.player2.increment_bounce_counter()
                self.player2.set_collision_with_ball(True)
                self.player1.reset_bounce_counter()
                self.player1.set_serving(False)
                pygame.mixer.Sound.play(self.bounce_ball_sound)
        else:
            self.player2.set_collision_with_ball(False)

        if self.check_collision(self.player1, self.ball):
            self.player1.set_start_rotation()
            if not self.player1.collision_with_ball():
                self.player1.increment_bounce_counter()
                self.player1.set_collision_with_ball(True)
                self.player2.reset_bounce_counter()
                self.player2.set_serving(False)
                pygame.mixer.Sound.play(self.bounce_ball_sound)
        else:
            self.player1.set_collision_with_ball(False)

        for key in self.frames:
            if self.check_collision(self.frames[key], self.ball):
                pygame.mixer.Sound.play(self.bounce_ball_sound)

    def check_if_point_is_gained(self):
        player1_gained = None
        if self.check_collision(self.ball, self.frames['ground_player1']) or self.player1.check_bounce_counter():
            self.wait(True)
            player1_gained = False
            self.player2.set_serving(True)
            self.player1.reset_bounce_counter()
            self.player2.reset_bounce_counter()
            self.player2.gained_point()
            if self.player2.get_score() - self.player1.get_score() > 1:
                self.player2.set_dominance(True)
            else:
                self.player2.set_dominance(False)
        elif self.check_collision(self.ball, self.frames['ground_player2']) or self.player2.check_bounce_counter():
            self.wait(True)
            player1_gained = True
            self.player1.set_serving(True)
            self.player2.reset_bounce_counter()
            self.player1.reset_bounce_counter()
            self.player1.gained_point()
            if self.player1.get_score() - self.player2.get_score() > 1:
                self.player1.set_dominance(True)
            else:
                self.player1.set_dominance(False)
        if self.is_waiting():
            self.player1.definitive_stop()
            self.player2.definitive_stop()
            self.ball.stop()
            self.player1.save_position()
            self.player2.save_position()
            self.ball.save_position()
            self.ball.set_position((0, 2 * self.window.y))
            self.player1.set_position((-2 * self.window.x, 2 * self.window.y))
            self.player2.set_position((2 * self.window.x, 2 * self.window.y))
            Game.gained_point = {'player1': player1_gained, 'player2': not player1_gained}

    def break_after_gained_point(self):
        if Game.break_timer >= 20:
            self.update_general_score_text()
            self.ball.stop()
            self.player1.definitive_stop()
            self.player2.definitive_stop()
            if not self.player1.is_sleeping():
                self.player1.sleep()
            if not self.player2.is_sleeping():
                self.player2.sleep()
            Game.break_timer = 0
            self.wait(False)
            self.player1.set_position_to_start_pos()
            self.player2.set_position_to_start_pos()
            if Game.gained_point['player1']:
                self.ball.set_position_to_start_pos(self.ball.get_start_positions()['player1'])
            else:
                self.ball.set_position_to_start_pos(self.ball.get_start_positions()['player2'])
            self.ball.set_start_rotation()
            self.ball.stop()
            self.ball.sleep()
            self.check_if_someone_won()
            Game.gained_point = {'player1': False, 'player2': False}
        else:
            Game.break_timer += 1

    def interface(self):
        list_of_events = pygame.event.get()
        for event in list_of_events:
            if event.type == pygame.QUIT:
                self.exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and not self.end_game():
                    if self.is_paused():
                        self.resume()
                    else:
                        self.pause()
                if event.key == pygame.K_r and self.end_game():
                    self.restart()
                if event.key == pygame.K_v:
                    self.handle_music()
                if event.key == pygame.K_ESCAPE:
                    self.exit_game()

        if not self.is_waiting() and not self.is_paused():
            self.update_player1(list_of_events)
            self.update_player2(list_of_events)
            self.check_if_ball_collides_with_sth()
            self.check_if_point_is_gained()
        elif not self.is_paused():
            self.break_after_gained_point()

    def step(self):
        self.space.step(Game.STEP_WORLD)

        self.draw_background(self.screen, self.background)
        self.space.debug_draw(self.draw_options)
        self.draw_help_background()

        self.draw_text(self.game_texts['general_score_text'].to_draw())

        if self.is_paused() and not self.end_game():
            self.draw_text(self.game_texts['press_resume_text'].to_draw())
            self.draw_text(self.game_texts['press_quit_text'].to_draw())
        elif not self.end_game():
            self.draw_text(self.game_texts['press_pause_text'].to_draw())
            self.draw_text(self.game_texts['press_quit_text'].to_draw())
        if pygame.mixer.music.get_busy():
            self.draw_text(self.game_texts['press_stop_music_text'].to_draw())
        else:
            self.draw_text(self.game_texts['press_play_music_text'].to_draw())

        self.draw_text(self.game_texts['copyright_text'].to_draw())

        self.ball.check_velocity_restrictions()

        if not self.is_waiting():
            self.draw_ball()
            self.draw_players()
        else:
            self.fake_draw_ball()
            self.fake_draw_players()

        if self.is_paused() and not self.end_game():
            self.draw_text(self.game_texts['pause_text'].to_draw())
        elif self.end_game():
            self.draw_text(self.game_texts['winner_text'].to_draw())
            self.draw_text(self.game_texts['restart_text'].to_draw())
            self.draw_text(self.game_texts['quit_text'].to_draw())

        pygame.display.flip()
        self.fpsClock.tick(self.FPS)

    @staticmethod
    def create_space(gravity):
        space = pymunk.Space()
        space.gravity = gravity
        space.sleep_time_threshold = 1
        return space

    @staticmethod
    def create_frames(space, window, scale_factor):
        return {'wall_left': Wall(space, (-10 * scale_factor['x'], 0), (-10 * scale_factor['x'], window.y),
                                  10 * scale_factor['x']),
                'wall_right': Wall(space, (window.x + 10 * scale_factor['x'], 0), (window.x + 10 * scale_factor['x'],
                                                                                   window.y), 10 * scale_factor['x']),
                'ceil': Wall(space, (0, window.y + 10 * scale_factor['y']),
                             (window.x, window.y + 10 * scale_factor['y']), 10 * scale_factor['y']),
                'net': Net(space, (window.x / 2, 0), (window.x / 2, 7 * window.y / 24),
                           Net.THICKNESS * scale_factor['x']),
                'ground_player1': Ground(space, (window.x / 2, window.y / 22 - 10 * scale_factor['y']),
                                         (window.x, window.y / 22 - 10 * scale_factor['y']), 10 * scale_factor['y']),
                'ground_player2': Ground(space, (0, window.y / 22 - 10 * scale_factor['y']),
                                         (window.x / 2, window.y / 22 - 10 * scale_factor['y']),
                                         10 * scale_factor['y'])}

    @staticmethod
    def create_texts(window, scale_factor):
        general_score_text = Text(Text.MAIN_FONT, scale_factor['xy'], Text.BLACK, '0:0', window.x / 2, 0.25 * window.y)
        pause_text = Text(Text.MAIN_FONT, 3 * scale_factor['xy'], Text.RED, 'PAUSE', window.x / 2, window.y / 2)
        winner_text = None
        restart_text = Text(Text.MAIN_FONT, 0.7 * scale_factor['xy'], Text.RED, 'PRESS R TO RESTART GAME',
                            window.x / 2, 0.65 * window.y)
        quit_text = Text(Text.MAIN_FONT, 0.5 * scale_factor['xy'], Text.RED, 'PRESS ESC TO QUIT GAME',
                         window.x / 2, 0.75 * window.y)
        press_stop_music_text = Text(Text.MAIN_FONT, 0.2 * scale_factor['xy'], Text.BLACK, 'PRESS V TO STOP MUSIC')
        press_stop_music_text.set_text_center((window.x - press_stop_music_text.text_size.x / 2,
                                               press_stop_music_text.text_size.y / 2))
        press_play_music_text = Text(Text.MAIN_FONT, 0.2 * scale_factor['xy'], Text.BLACK, 'PRESS V TO PLAY MUSIC')
        press_play_music_text.set_text_center((window.x - press_play_music_text.text_size.x / 2,
                                               press_play_music_text.text_size.y / 2))
        press_pause_text = Text(Text.MAIN_FONT, 0.2 * scale_factor['xy'], Text.BLACK, 'PRESS P TO PAUSE GAME')
        press_pause_text.set_text_center((window.x - press_pause_text.text_size.x / 2,
                                          press_pause_text.text_size.y / 2 + press_play_music_text.text_size.y))
        press_resume_text = Text(Text.MAIN_FONT, 0.2 * scale_factor['xy'], Text.BLACK, 'PRESS P TO RESUME GAME')
        press_resume_text.set_text_center((window.x - press_resume_text.text_size.x / 2,
                                           press_resume_text.text_size.y / 2 + press_play_music_text.text_size.y))
        press_quit_text = Text(Text.MAIN_FONT, 0.2 * scale_factor['xy'], Text.BLACK, 'PRESS ESC TO QUIT GAME')
        press_quit_text.set_text_center((window.x - press_quit_text.text_size.x / 2,
                                         press_quit_text.text_size.y / 2 + press_stop_music_text.text_size.y +
                                         press_pause_text.text_size.y))
        copyright_text = Text(Text.MAIN_FONT, 0.15 * scale_factor['xy'], Text.BLACK, '© Michał Dybowski, 2019')
        copyright_text.set_text_center((window.x - copyright_text.text_size.x / 2,
                                        window.y - copyright_text.text_size.y / 2))

        return {'general_score_text': general_score_text, 'pause_text': pause_text,
                'winner_text': winner_text, 'restart_text': restart_text, 'quit_text': quit_text,
                'press_pause_text': press_pause_text, 'press_resume_text': press_resume_text,
                'press_stop_music_text': press_stop_music_text, 'press_play_music_text': press_play_music_text,
                'press_quit_text': press_quit_text, 'copyright_text': copyright_text}

    @staticmethod
    def check_collision(ob1, ob2):
        return bool(ob1.get_shape().shapes_collide(ob2.get_shape()).points)

    @staticmethod
    def load_image(window_size, source, with_convert):
        if with_convert:
            picture = pygame.image.load(source).convert()
        else:
            picture = pygame.image.load(source)
        return pygame.transform.scale(picture, window_size)

    @staticmethod
    def draw_background(screen, image):
        screen.blit(image, (0, 0))

    def draw_help_background(self):
        surf = pygame.Surface((self.window.x, self.window.y / 22))
        surf.blit(self.background, (0, -self.window.y + self.window.y / 22))
        self.screen.blit(surf, (0, self.window.y - self.window.y / 22))

    def draw_text(self, text):
        self.screen.blit(text[0], text[1])

    def draw_players(self):
        self.screen.blit(self.player1_image, (self.player1.get_position().x - self.player1.get_radius(),
                                              self.window.y - self.player1.get_position().y -
                                              self.player1.get_radius()))
        self.screen.blit(self.player2_image, (self.player2.get_position().x - self.player2.get_radius(),
                                              self.window.y - self.player2.get_position().y -
                                              self.player2.get_radius()))

    def fake_draw_players(self):
        self.screen.blit(self.player1_image, (self.player1.get_position_to_breaks().x - self.player1.get_radius(),
                                              self.window.y - self.player1.get_position_to_breaks().y -
                                              self.player1.get_radius()))
        self.screen.blit(self.player2_image, (self.player2.get_position_to_breaks().x - self.player2.get_radius(),
                                              self.window.y - self.player2.get_position_to_breaks().y -
                                              self.player2.get_radius()))

    def draw_ball(self):
        surf = pygame.transform.rotate(self.ball_image, math.degrees(self.ball.get_body_angle()))
        w, h = surf.get_size()
        p = pymunk.pygame_util.to_pygame(self.ball.get_position() + pymunk.Vec2d(-w / 2, h / 2), self.screen)
        self.screen.blit(surf, p)

    def fake_draw_ball(self):
        surf = pygame.transform.rotate(self.ball_image, math.degrees(self.ball.get_position_to_breaks()['angle']))
        w, h = surf.get_size()
        p = pymunk.pygame_util.to_pygame(self.ball.get_position_to_breaks()['pos'] + pymunk.Vec2d(-w / 2, h / 2),
                                         self.screen)
        self.screen.blit(surf, p)

    @staticmethod
    def handle_music():
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.play(-1)

    @staticmethod
    def exit_game():
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()


def open_settings(settings_path):
    try:
        with open(settings_path, 'r') as settings:
            f_line = settings.readline().split()
            window_size = (int(f_line[1].replace(',', '')), int(f_line[2]))
            fps = int(settings.readline().split()[1])
    except IOError:
        print("Can't load settings")
        print('Opening with settings: window_size = (1200, 650); fps = 60')
        window_size = (1200, 650)
        fps = 60

    return window_size, fps


def sign(x):
    if x > 0:
        return 1
    else:
        return -1


def run_game():

    window_size, fps = open_settings(Game.SETTINGS)

    game = Game(window_size, fps)

    while True:

        game.interface()

        game.step()


if __name__ == '__main__':

    run_game()
