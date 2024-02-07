import math
import pygame
import random
import os

# class Game():
#     def __init__(self, FPS):
#         self.BOLD_FONT = pygame.font.Font(os.path.abspath('fonts/bold_font.ttf'), 21)
#         self.NORM_FONT = pygame.font.Font(os.path.abspath('fonts/norm_font.ttf'), 16)
#         self.score = 1
#         self.score_board = self.BOLD_FONT.render(
#             f"Round: {self.score}", True, (240, 240, 240), (115, 117, 117))
#         self.player = Player()
#         self.player_group = pygame.sprite.Group(self.player)
#         self.bullet_group = pygame.sprite.Group()
#         self.countdown_group = pygame.sprite.Group()
#         self.wait_time = 0
#         self.wait_delay = 2 * FPS
#         self.bullet_spawn_time = 0
#         self.bullet_spawn_delay = FPS
#         self.current_bullet_count = 5
#         self.max_bullet_count = self.current_bullet_count
#         self.prepare_time = 0
#         self.prepare_delay = 5 * FPS
#         self.state = "PREPARE"
#         self.wave = 1


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((24, 24))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.move = False
    
    def update(self, width, height):
        if not self.move:
            return
        self.rect.center = pygame.mouse.get_pos()
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= width:
            self.rect.right = width
        elif self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= height:
            self.rect.bottom = height

    # def draw(self, screen):
    #     screen.blit(self, self.rect.center)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, FPS, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.check_outside = False
        vel = random.randint(4, 7) * 60

        # Because rect.x and rect.y are automatically converted
        # to integers, we need to create different variables that
        # store the location as floating point numbers. Integers
        # are not accurate enough for aiming.
        self.floating_point_x = pos_x
        self.floating_point_y = pos_y

        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        mpos_x, mpos_y = pygame.mouse.get_pos()
        x_diff = mpos_x - pos_x
        y_diff = mpos_y - pos_y
        angle = math.atan2(y_diff, x_diff)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        self.change_x = math.cos(angle) * vel
        self.change_y = math.sin(angle) * vel

    def update(self, delta, width, height):
        # The floating point x and y hold our more accurate location.
        self.floating_point_y += self.change_y * delta
        self.floating_point_x += self.change_x * delta
        # print(f"1: {self.floating_point_x} 2: {self.floating_point_y}")
        # print(f"3: {self.change_x} 4: {self.change_y}")
        # The rect.x and rect.y are converted to integers.
        self.rect.center = (int(self.floating_point_x),
                            int(self.floating_point_y))
        # print(f"3: {self.rect.center}")

        # If the bullet flies of the screen, get rid of it.
        if (self.rect.centerx < -50 or self.rect.centerx > width + 50 or self.rect.centery < -50 and self.rect.centery > height + 50):
            self.check_outside = True
        if (self.rect.right < 0 or self.rect.left > width or self.rect.top < 0 or self.rect.bottom > height) and self.check_outside:
            self.kill()

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text='', font=None, color=(73, 73, 73), highlight_color=(189, 189, 189), function=None, text_color=(0, 0, 0)):
        super().__init__()  # Initialize the sprite
        self.image = pygame.Surface((width, height))
        self.color = color
        self.highlight_color = highlight_color
        self.function = function
        self.text = text
        self.text_color = text_color
        self.font =  font
        self.rect = self.image.get_rect(center=(x, y))
        self.is_hovered = False
        self.update_text()

    def update_text(self):
        self.image.fill(self.highlight_color if self.is_hovered else self.color)
        if self.text != '':
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.rect.width / 2, self.rect.height / 2))
            self.image.blit(text_surface, text_rect)

    def update(self, event_list):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered:
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.function:
                        self.function()
        self.update_text()
        

class CurvedBullet(pygame.sprite.Sprite):
    def __init__(self, FPS, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill((0, 255, 0))  # Red bullet
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.check_outside = False
        
        # Adjusted velocity to be consistent with your FPS scaling
        self.speed = random.randint(6, 8) * 60 # Maintain consistent speed across FPS
        
        self.floating_point_x = float(pos_x)
        self.floating_point_y = float(pos_y)

        # Calculate initial direction towards mouse position
        mpos_x, mpos_y = pygame.mouse.get_pos()
        self.angle = math.atan2(mpos_y - pos_y, mpos_x - pos_x)

        # Curvature: adjust for noticeable curve
        self.curvature = random.uniform(-1, 1)  # Adjust as needed for visible curvature
        
        # Initialize velocity components based on angle
        self.change_x = math.cos(self.angle) * self.speed
        self.change_y = math.sin(self.angle) * self.speed

    def update(self, delta, width, height):
        # Apply curvature by adjusting the bullet's angle and then its direction
        self.angle += self.curvature * delta
        
        # Recalculate velocity to maintain speed but change direction
        self.change_x = math.cos(self.angle) * self.speed
        self.change_y = math.sin(self.angle) * self.speed
        
        # Update position with constant speed
        self.floating_point_x += self.change_x * delta
        self.floating_point_y += self.change_y * delta
        
        self.rect.x = int(self.floating_point_x)
        self.rect.y = int(self.floating_point_y)
        # print(f"3: {self.rect.center}")

        # If the bullet flies of the screen, get rid of it.
        if (self.rect.centerx < -50 or self.rect.centerx > width + 50 or self.rect.centery < -50 and self.rect.centery > height + 50):
            self.check_outside = True
        if (self.rect.right < 0 or self.rect.left > width or self.rect.top < 0 or self.rect.bottom > height) and self.check_outside:
            self.kill()