import numpy as np
import pygame
from map.map import Map
from characters.player import Player
from random import randint
import math as mth
from icecream import ic

from config import BotConfig, MapConfig, SprinterBotConfig, WindowConfig


class Bot(Player):
    def __init__(self, player: Player) -> None:
        super().__init__()
        self.config = BotConfig()
        self._player: Player = player
        self.type: str = "default"
        self.obstacles = Map().obstacles

        # Choosing where to spawn
        while True:
            self.x: int = randint(-WindowConfig().width, WindowConfig().width)
            self.y: int = randint(-WindowConfig().height, WindowConfig().height)
            self.spawn_distance_from_player: float = np.sqrt(
                (
                    self.x
                    + self.config.height / 2
                    - self._player.x
                    - self._player.width / 2
                )
                ** 2
                + (
                    self.y
                    + self.config.height / 2
                    - self._player.y
                    - self._player.height / 2
                )
                ** 2
            )
            if (
                self.config.max_spawn_radius
                >= self.spawn_distance_from_player
                >= self.config.min_spawn_radius
            ):
                break

    def draw_bot(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            self.config.color,
            (
                self.x,
                self.y,
                self.config.height,
                self.config.height,
            ),
        )

    def _get_vector_to_player_parameters(self, bot_width, bot_height) -> np.ndarray:
        vector_to_player: np.ndarray = np.array(
            [
                self.x + bot_width / 2 - (self._player.x + self._player.width / 2),
                self.y + bot_height / 2 - (self._player.y + self._player.height / 2),
            ]
        )
        return vector_to_player

    def is_colliding(
        self,
        future_x: float,
        future_y: float,
    ) -> bool:
        """
        If new position is coliding with any obstacle on the map or with the player returns `True`.
        """
        bot_rect = pygame.Rect(
            future_x, future_y, self.config.width, self.config.height
        )

        # Collisions with obstacles
        # if self.obstacles:
        #     for obstacle in self.obstacles:
        #         obstacle_rect = pygame.Rect(
        #             obstacle.x, obstacle.y, obstacle.width, obstacle.height
        #         )
        #         if bot_rect.colliderect(obstacle_rect):
        #             return True

        # Collisions with player
        player_rect = pygame.Rect(
            self._player.x, self._player.y, self._player.width, self._player.height
        )
        if bot_rect.colliderect(player_rect):
            return True

        return False

    def spawn(self):
        x = randint(0, MapConfig().width - self.width)
        self.x = x
        self.y = 0

    def die(self):
        self.spawn()

    def move_to_player(self):
        vector: np.ndarray = self._get_vector_to_player_parameters(
            self.config.height, self.config.height
        )

        # Random movement, but most likely towards player
        angle = np.random.normal(0, 80)
        angle_rad = mth.radians(angle)

        dx, dy = vector
        cos_theta, sin_theta = mth.cos(angle_rad), mth.sin(angle_rad)
        rotated_vector = np.array(
            [
                dx * cos_theta - dy * sin_theta,
                dx * sin_theta + dy * cos_theta,
            ]
        )

        rotated_vector_normalized = rotated_vector / np.linalg.norm(rotated_vector)
        new_x = self.x - rotated_vector_normalized[0] * self.config.speed
        new_y = self.y - rotated_vector_normalized[1] * self.config.speed

        if self.is_colliding(new_x, new_y):
            self.die()
        else:
            self.x = new_x
            self.y = new_y


class BotSprinter(Bot):
    def __init__(self, player: Player) -> None:
        super().__init__(player)
        self.config = SprinterBotConfig()
        self.type: str = "sprinter"
        self.start_time = None
        self.current_speed = 0
        self.moving = True

    def draw_bot(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            self.config.color,
            (
                self.x,
                self.y,
                self.config.width,
                self.config.height,
            ),
        )

    def move_to_player(self):
        if self.start_time is None or not self.moving:
            self.start_time = pygame.time.get_ticks()
            self.current_speed = 0
            self.moving = True
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000

        # Acceleration
        if elapsed_time < self.config.time_to_max_speed:
            self.current_speed = self.config.speed * (
                elapsed_time / self.config.time_to_max_speed
            )
        else:
            self.current_speed = self.config.speed

        vector: np.ndarray = self._get_vector_to_player_parameters(
            self.config.width, self.config.height
        )
        vector_normalized = vector / np.linalg.norm(vector)

        new_x = self.x - vector_normalized[0] * self.current_speed
        new_y = self.y - vector_normalized[1] * self.current_speed

        if self.is_colliding(new_x, new_y):
            self.moving = False
            self.die()
        else:
            self.x = new_x
            self.y = new_y


def main() -> None:
    bot_sprinter = BotSprinter(Player())
    print()
    bot_sprinter = Bot(Player())


if __name__ == "__main__":
    main()