import pygame
from simulation import Simulation
from bullet import Bullet
from config import *


class Renderer:
    def __init__(self, simulation: Simulation):
        pygame.init()

        self.simulation = simulation
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.w_pressed = False
        self.s_pressed = False
        self.a_pressed = False
        self.d_pressed = False
        self.mouse_pressed = False

    def draw_player(self):
        pygame.draw.rect(
            self.screen,
            PLAYER_COLOR,
            (
                self.simulation.player.x,
                self.simulation.player.y,
                PLAYER_WIDTH,
                PLAYER_HEIGHT,
            ),
        )

    def draw_frame(self):
        self.screen.fill(BG_COLOR)
        self.draw_player()
        for bullet in self.simulation.bullets:
            bullet.draw(self.screen)

        for bot in self.simulation.bots:
            bot.draw_bot(self.screen)

        pygame.display.flip()

    def handle_keyborad_input(self, event):
        if event.type == pygame.QUIT:
            self.simulation.game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.w_pressed = True
            elif event.key == pygame.K_s:
                self.s_pressed = True
            elif event.key == pygame.K_a:
                self.a_pressed = True
            elif event.key == pygame.K_d:
                self.d_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.w_pressed = False
            elif event.key == pygame.K_s:
                self.s_pressed = False
            elif event.key == pygame.K_a:
                self.a_pressed = False
            elif event.key == pygame.K_d:
                self.d_pressed = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouse_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_pressed = False

    def player_move(self):
        dx = 0
        dy = 0
        if self.w_pressed:
            dy -= PLAYER_SPEED
        if self.s_pressed:
            dy += PLAYER_SPEED
        if self.a_pressed:
            dx -= PLAYER_SPEED
        if self.d_pressed:
            dx += PLAYER_SPEED
        self.simulation.player.move(dx, dy)

    def run(self):
        while not self.simulation.game_over:
            for event in pygame.event.get():
                self.handle_keyborad_input(event)
            self.player_move()

            for bot in self.simulation.bots:
                bot.move_to_player()

            if self.mouse_pressed:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.simulation.bullets.append(
                    Bullet(self.simulation.player, mouse_x, mouse_y)
                )

            for bullet in self.simulation.bullets:
                bullet.update()

            self.draw_frame()
            self.simulation.next_step()
            self.clock.tick(GAME_FPS)
