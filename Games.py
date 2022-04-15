from cgitb import text
import sys
import random
from telnetlib import GA
from tkinter import font

import pygame
from pygame.locals import *

pygame.init()

player_one = 'Player.png'
player_bullet = 'bullet.png'
enemy_one = 'enemy01.png'
enemy_bullet = 'enemy_beam01.png'
font = pygame.font.SysFont('Arial',30)


screen = pygame.display.set_mode((0,0),FULLSCREEN)
s_width,s_height = screen.get_size()

clock = pygame.time.Clock()
FPS = 60

background_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
playerbullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemybullet_group = pygame.sprite.Group()
sprite_group = pygame.sprite.Group()

class Background(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface([x,y])
        self.image.fill('yellow')
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 1
        self.rect.x += 1
        if self.rect.y >s_height:
            self.rect.y = random.randrange(-10,0)
            self.rect.x = random.randrange(-400,s_width)

class Player (pygame.sprite.Sprite):

    def __init__(self,img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        # self.image.set_colorkey('black')

    def update(self):
        mouse = pygame.mouse.get_pos()
        self.rect.x = mouse[0]
        self.rect.y = mouse[1]

    def shoot(self):
        bullet = PlayerBullet(player_bullet)
        mouse = pygame.mouse.get_pos()
        bullet.rect.x = mouse[0]
        bullet.rect.y = mouse[1]
        playerbullet_group.add(bullet)
        sprite_group.add(bullet)

class Enemy(Player):

    def __init__(self,img):
        super().__init__(img)
        self.rect.x = random.randrange(0,s_width)
        self.rect.y = random.randrange(-500,0)
        screen.blit(self.image,(self.rect.x,self.rect.y))

    def update(self):
        self.rect.y += 1
        if self.rect.y >s_height:
            self.rect.x = random.randrange(0, s_width)
            self.rect.y = random.randrange(-2000, 0)
        self.shoot_enemy()
    def shoot_enemy(self):
        if self.rect.y in (0,100,250,500):
            enemybullet = EnemyBullet(enemy_bullet)
            enemybullet.rect.x = self.rect.x + 15
            enemybullet.rect.y = self.rect.y + 40
            enemybullet_group.add(enemybullet)
            sprite_group.add(enemybullet)


class PlayerBullet(pygame.sprite.Sprite):

    def __init__(self,img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (50,50))
        self.image = pygame.transform.rotate(self.image,90)
        self.rect = self.image.get_rect()
        # self.image.set_colorkey('black')

    def update(self):
        self.rect.y -=5
        if self.rect.y<0:
            self.kill()

class EnemyBullet(PlayerBullet):

    def __init__(self,img):
        super().__init__(img)
        self.image = pygame.transform.scale(self.image, (20, 20))

    def update(self):
        self.rect.y += 3
        if self.rect.y > s_height:
            self.kill()



class Game :
    
    def __init__(self):
        self.count_hit = 0
        self.score_value = 0
        self.run_game()

    def create_background(self):
        for i in range(50):
            x = random.randint(1,7)
            background_image = Background(x,x)
            background_image.rect.x = random.randrange(0,s_width)
            background_image.rect.y = random.randrange(0,s_height)
            background_group.add(background_image)
            sprite_group.add(background_image)
        


    def create_player(self):
        self.player = Player(player_one)
        player_group.add(self.player)
        sprite_group.add(self.player)
    
    def create_enemy(self):
        for i in range (10):
            self.enemy = Enemy(enemy_one)
            enemy_group.add(self.enemy)
            sprite_group.add(self.enemy)
    
    def playerbullet_hits_enemy(self):
        hits = pygame.sprite.groupcollide(enemy_group,playerbullet_group, False, True)
        for i in hits :
            self.count_hit +=1
            if self.count_hit == 2:
                self.score_value += 100
                i.rect.x = random.randrange(0,s_width)
                i.rect.y = random.randrange(-3000,-100)
                self.count_hit = 0
    def show_score(self):
        score = font.render('Score : ' + str(self.score_value), True, ('white'))
        screen.blit(score,(50,50))

    
    def run_update(self):
        sprite_group.draw(screen)
        sprite_group.update()

    def run_game(self):
        self.create_background()
        self.create_player()
        self.create_enemy()
        while True:
            screen.fill('black')
            self.show_score()
            self.playerbullet_hits_enemy()
            self.run_update()
            for event in pygame.event.get():
                if event.type == QUIT: 
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        self.player.shoot()
            pygame.display.update()
            clock.tick(FPS)

def main():
    game = Game()

if __name__ == '__main__':
    main()

Game.playerbullet_hits_enemy()