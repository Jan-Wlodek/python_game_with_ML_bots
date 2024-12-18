import pygame
import math
import random
import characters.entity as ent

from config import BulletConfig, BotConfig
#from map.obstacle import Obstacle


class Bullet(ent.Entity):

    def __init__(self, author, direction, mode="single"):
        super().__init__()
        self.author = author
        self.x = author.x
        self.y = author.y
        self.speed = BulletConfig().speed
        self.damage = BulletConfig().damage
        self.radius = BulletConfig().radius
        self.direction = direction
        self.config = BulletConfig()
        
        self.size = [2*self.radius,2*self.radius]

        self.bot_width = BotConfig().width
        self.bot_height = BotConfig().height
        if author.collision_layer == ent.CollisionLayers.PLAYER:
            self.collision_layer = ent.CollisionLayers.BULLET
            self.collision_interactions = {ent.CollisionLayers.BOT : ent.CollisionInteractions.SACRIFICE}
        else:
            self.collision_layer = ent.CollisionLayers.BULLET_BOT
            self.collision_interactions = {ent.CollisionLayers.PLAYER : ent.CollisionInteractions.SACRIFICE}
            
        self.collision_interactions[ent.CollisionLayers.GROUND] = ent.CollisionInteractions.SACRIFICE

        if mode == "shotgun":
            spread_angle = 0.2  # value in radians (1 radian = 57.2958 degrees)
            self.direction += random.uniform(-spread_angle, spread_angle)
            self.speed -= 4

    def update(self):
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed

    def draw(self, screen: pygame.Surface, offset_x=0, offset_y=0):
        pygame.draw.circle(
            screen,
            BulletConfig().color,
            (int(self.x - offset_x), int(self.y - offset_y)),
            BulletConfig().radius,
        )

    def check_bullet_collision_with_object(self, obj):
        if self.author == obj:
            return False
        bullet_left = self.x - self.radius
        bullet_right = self.x + self.radius
        bullet_top = self.y - self.radius
        bullet_bottom = self.y + self.radius

        obstacle_left = obj.x
        obstacle_right = obj.x + obj.width
        obstacle_top = obj.y
        obstacle_bottom = obj.y + obj.height
        if not (
            bullet_right <= obstacle_left
            or bullet_left >= obstacle_right
            or bullet_bottom <= obstacle_top
            or bullet_top >= obstacle_bottom
        ):
            return True

        return False