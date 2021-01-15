import pygame
from pygame.constants import (
    QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_TAB, K_KP_PLUS, K_KP_MINUS, K_F10, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE)
import os
import random
import time


class Settings:
    """
    Static class of project settings.

    This static class contains project global settings.
    """
    window_width = 600
    window_height = 688
    fps = 60
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")

    @staticmethod
    def get_dim():
        """
        Returns:
            (int, int): Width and height of the window.
        """
        return (Settings.window_width, Settings.window_height)


class Globals:
    """
    Static class of project global variables.

    This static class contains project global variables.
    """
    points = 0


class Background(pygame.sprite.Sprite):
    """
    Background sprite class.

    This class is derived from pygame.sprite.Sprite and manages the background bitmap.
    """

    def __init__(self, filename):
        """Constructor.

        Args:
            filename (string): Name - without path - of the background bitmap.
        """
        super().__init__()
        self.image = pygame.image.load(os.path.join(
            Settings.image_path, filename)).convert()
        self.image = pygame.transform.scale(self.image, Settings.get_dim())
        self.rect = self.image.get_rect()

    def draw(self, screen):
        """Draws the background bitmap on the screen.

        Args:
            screen (pygame.display): Window display.
        """
        screen.blit(self.image, self.rect)


class Spaceship(pygame.sprite.Sprite):
    """Spaceship sprite class.

    This class is derived from pygame.sprite.Sprite and manages the background bitmap.
    """

    def __init__(self):
        """Constructor.
        """
        super().__init__()
        self.images = []
        self.images.append(pygame.image.load(os.path.join(
            Settings.image_path, "raumschiff02.png")).convert_alpha())
        self.images.append(pygame.image.load(os.path.join(
            Settings.image_path, "raumschiff03.png")).convert_alpha())
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.startpos()
        self.speed = 4
        self.speed_h = 0
        self.speed_v = 0
        self.time_between_jump = 2000
        self.time_next_possible_jump = pygame.time.get_ticks()

    def draw(self, screen):
        """Draws the bitmap on the screen.

        Args:
            screen (pygame.display): Window display
        """
        index = 0 if (self.can_jump()) else 1
        self.image = self.images[index]
        screen.blit(self.image, self.rect)

    def update(self):
        """Updates the status of the sprite.
        """
        newpos = self.rect.move(self.speed_h, self.speed_v)
        if newpos.left >= 0 and newpos.right <= Settings.window_width:
            if newpos.top >= 0 and newpos.bottom <= Settings.window_height:
                self.rect = newpos

    def startpos(self):
        """Computes the start position.
        """
        self.rect.bottom = Settings.window_height - 10
        self.rect.centerx = Settings.window_width // 2


    def can_jump(self):
        """Checks if the spaceship can jump.

        Returns:
            bool: True if the conditions allows a jump else False.
        """
        return pygame.time.get_ticks() >= self.time_next_possible_jump

    def jump(self):
        """Jumps to a new randomly choosen position.
        """
        if self.can_jump():
            self.rect.left = random.randint(
                0, Settings.window_width-self.rect.width)
            self.rect.top = random.randint(
                0, Settings.window_height-self.rect.height)
            self.time_next_possible_jump = pygame.time.get_ticks() + self.time_between_jump

    def move_stop(self):
        """Manages the horizontal and vertical speed in order to stop moving.
        """
        self.speed_h = self.speed_v = 0

    def move_left(self):
        """Manages the horizontal speed in order to move left.
        """
        self.speed_h = -1 * self.speed

    def move_right(self):
        """Manages the horizontal speed in order to move right.
        """
        self.speed_h = 1 * self.speed

    def move_up(self):
        """Manages the vertical speed in order to move up.
        """
        self.speed_v = -1 * self.speed

    def move_down(self):
        """Manages the vertical speed in order to move down.
        """
        self.speed_v = 1 * self.speed


class Lifes(pygame.sprite.Sprite):
    """Presentation of available lifes.

    This class is derived from pygame.sprite.Sprite and manages the lifes bitmap.
    """

    def __init__(self):
        """Constructor.
        """
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.image_path, "raumschiff.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.set_startpos()
        self.number = 3

    def draw(self, screen):
        """Draws the bitmap on the screen.

        Args:
            screen (pygame.display): Window display
        """
        self.set_startpos()
        for i in range(0, self.number):
            screen.blit(self.image, self.rect)
            self.rect.move_ip(-self.rect.width, 0)

    def inc(self):
        """Increments the number of lifes
        """
        if self.number > 0:
            self.number -= 1 

    def set_startpos(self):
        self.rect.top = 10
        self.rect.right = Settings.window_width


class Rock(pygame.sprite.Sprite):
    """Rock sprite class.

    This class is derived from pygame.sprite.Sprite and manages one rock bitmap.
    """

    def __init__(self):
        """Constructor.
        """
        super().__init__()
        r = random.randint(0, 9)
        self.image = pygame.image.load(os.path.join(
            Settings.image_path, f"felsen{r}.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.speed = random.randint(1, 4)
        self.randompos()

    def randompos(self):
        """Computes a new random horizontal position.
        """
        self.rect.left = random.randint(
            0, Settings.window_width - self.rect.width)

    def update(self):
        """Updates the status of the sprite.
        """
        self.rect.move_ip(0, self.speed)
        if self.rect.top > Settings.window_height:
            self.kill()
            Globals.points += 1

    def draw(self, screen):
        """Draws the bitmap on the screen.

        Args:
            screen (pygame.display): Window display
        """
        screen.blit(self.image, self.rect)


class Game(object):
    """The Game class.

    This class is manages all components and logics of the game.
    """

    def __init__(self):
        """Constructor.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.get_dim())
        pygame.display.set_caption("Fingerübung \"Rocks\"")
        self.clock = pygame.time.Clock()
        self.lifes = Lifes()
        self.background = Background("space01.png")
        self.spaceship = Spaceship()
        self.all_rocks = pygame.sprite.Group()
        self.time_between_rockbirth = 500
        self.time_next_possible_rockbirth = pygame.time.get_ticks()
        self.time_between_time_decrement = 2000
        self.time_next_possible_time_decrement = pygame.time.get_ticks()
        self.font_normalsize = pygame.font.Font(
            pygame.font.get_default_font(), 12)
        self.font_bigsize = pygame.font.Font(
            pygame.font.get_default_font(), 40)

    def watch_for_events(self):
        """Reaction of keyboard and other system events events.
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_LEFT:
                    self.spaceship.move_left()
                elif event.key == K_RIGHT:
                    self.spaceship.move_right()
                elif event.key == K_UP:
                    self.spaceship.move_up()
                elif event.key == K_DOWN:
                    self.spaceship.move_down()
                elif event.key == K_SPACE:
                    self.jump()
            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                    self.spaceship.move_stop()

    def draw(self):
        """Draws all bitmaps in meaningful order on the screen.
        """
        self.background.draw(self.screen)
        self.spaceship.draw(self.screen)
        self.all_rocks.draw(self.screen)
        self.draw_points()
        self.lifes.draw(self.screen)
        pygame.display.flip()

    def update(self):
        """Updates the status of the sprites and all other game components.
        """
        self.dec_time_between_rockbirth()
        self.rockbirth()
        self.spaceship.update()
        self.all_rocks.update()
        if pygame.sprite.spritecollide(self.spaceship, self.all_rocks, False):
            self.lifes.inc()
            if self.lifes.number <= 0:
                self.running = False
            else:
                self.all_rocks.empty()
                self.spaceship.startpos()

    def run(self):
        """Starting point of the game.

        Call this method in order to start the game. It contains the main loop.
        """
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()

        self.game_over()

        pygame.quit()

    def rockbirth(self):
        """Creates a new rock object.

        According to the time span between two rockbirths a rock will be created 
        and placed on a free spot.
        """
        if pygame.time.get_ticks() > self.time_next_possible_rockbirth:
            r = Rock()
            tries = 10
            while tries > 0:
                if pygame.sprite.spritecollide(r, self.all_rocks, False):
                    r.randompos()
                    tries -= 1
                else:
                    self.all_rocks.add(r)
                    break
            self.time_next_possible_rockbirth = pygame.time.get_ticks() + \
                self.time_between_rockbirth

    def draw_points(self):
        """Draws the number of points.
        """
        text = self.font_normalsize.render(
            f"Points: {Globals.points}", True, (255, 0, 0))
        self.screen.blit(text, (0, 10))

    def jump(self):
        """Tries to jump the spaceship to a free spot.
        """
        tries = 100
        while tries > 0:
            self.spaceship.jump()
            if pygame.sprite.spritecollide(self.spaceship, self.all_rocks, False):
                self.spaceship.jump()
                tries -= 1
            else:
                break

    def dec_time_between_rockbirth(self):
        """Descrements the duration between two rockbiths.
        """
        if pygame.time.get_ticks() >= self.time_next_possible_time_decrement:
            if self.time_between_rockbirth >= 50:
                self.time_between_rockbirth -= 10
            self.time_next_possible_time_decrement = pygame.time.get_ticks() + \
                self.time_between_time_decrement

    def game_over(self):
        """Game over behaviour.
        """
        text = self.font_bigsize.render("GAME OVER", True, (255, 0, 0))
        rect = text.get_rect()
        rect.centerx = Settings.window_width // 2
        rect.centery = Settings.window_height // 2 - 50
        self.screen.blit(text, rect)
        text = self.font_bigsize.render(
            f"Score: {Globals.points}", True, (0, 255, 0))
        rect = text.get_rect()
        rect.centerx = Settings.window_width // 2
        rect.centery = Settings.window_height // 2 + 50
        self.screen.blit(text, rect)
        pygame.display.flip()
        time.sleep(3)


if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 30"

    game = Game()
    game.run()
