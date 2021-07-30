import pygame
import os
import math

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """
        xe, ye = enemy.get_pos()
        xc, yc = self.center
        # distance_et: difference of an (e)nemy and a (t)ower
        distance_et = math.sqrt((xe - xc) ** 2 + (ye - yc) ** 2)
        if distance_et <= self.radius:
            return True
        else:
            return False

    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
        # create semi-transparent surface
        transparent_surface = pygame.Surface((300, 300), pygame.SRCALPHA)
        transparency = 50  # define transparency: 0~255, 0 is fully transparent
        # draw the rectangle on the transparent surface
        # x, y to get the position of center
        x, y = self.center
        pygame.draw.circle(transparent_surface, [220, 220, 220, transparency], [self.radius, self.radius], self.radius)
        win.blit(transparent_surface, (x - self.radius, y - self.radius))


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2  # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = False  # the state of whether the tower is selected
        self.type = "tower"

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """
        """
        Hint:
        let counter be 0
        if the counter < max counter then
            set counter to counter + 1
        else 
            counter return to zero
        end if
        """
        if self.cd_count < self.cd_max_count:
            self.cd_count += 1
        else:
            self.cd_count = 0
        if self.cd_count == 0:
            return False
        else:
            return True

    def attack(self, enemy_group):
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """
        # if the tower is not cool down
        if not self.is_cool_down():
            # if enemies in the attack range
            for enemy in enemy_group.get():
                if self.range_circle.collide(enemy):
                    # enemies get hurt
                    enemy.get_hurt(self.damage)
                    break

    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        # create semi-transparent surface
        transparent_surface = pygame.Surface((300, 300), pygame.SRCALPHA)
        transparency = 0  # define transparency: 0~255, 0 is fully transparent
        # draw the rectangle on the transparent surface
        # x, y to get the position of center
        xt, yt = self.rect.center
        xr, yr = self.rect
        pygame.draw.rect(transparent_surface, [0, 0, 0, transparency], [x, y, xr, yr])
        win.blit(transparent_surface, (x , y)
        """
        # x, y to get the position of center
        if self.rect.x <= x <= self.rect.x + self.rect.w and \
           self.rect.y <= y <= self.rect.y + self.rect.w:
            return True
        else:
            return False

    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower
