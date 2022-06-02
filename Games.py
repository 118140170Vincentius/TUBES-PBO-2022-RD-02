from cgitb import text
import sys
import random
from telnetlib import GA
from tkinter import font

import pygame
from pygame.locals import *
from pygame import mixer

pygame.init()

player_one = 'asset/Player.png'
player_bullet = 'asset/bullet.png'
enemy_one = 'asset/enemy01.png'
enemy_bullet = 'asset/enemy_beam01.png'
enemy2_bullet = 'asset/enemy_beam01.png'
font = pygame.font.SysFont('Arial',30)
bulletplayer_sound = 'asset/SoundEffect_Player.wav'
bgmusic = 'asset/bg_music1.wav'
enemy2  = 'asset/boss1.png'
enemy2_1  = 'asset/boss1.png'

player_pewpew = 'asset/laserShootPlayer.wav'
enemy_pewpew = 'asset/laserShootEnemy.wav'



screen = pygame.display.set_mode((1024,760),SHOWN)
s_width,s_height = screen.get_size()

clock = pygame.time.Clock()
FPS = 60

background_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
playerbullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy2_group = pygame.sprite.Group()
enemy2_1group = pygame.sprite.Group()
enemybullet_group = pygame.sprite.Group()
enemy2bullet_group = pygame.sprite.Group()
sprite_group = pygame.sprite.Group()

class Background(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface([x,y])
        self.image.fill('white')
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
        self.sound = pygame.mixer.Sound(player_pewpew)
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
    
    def soundeffect(self):
        pygame.mixer.Sound.set_volume(self.sound,0.5)
        self.sound.play()
        

class Enemy(Player):

    def __init__(self,img):
        super().__init__(img)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect.x = random.randrange(0,s_width)
        self.rect.y = random.randrange(-500,0)
        self.sound = pygame.mixer.Sound(enemy_pewpew)
        screen.blit(self.image,(self.rect.x,self.rect.y))

    def update(self):
        self.rect.y += 1
        if self.rect.y > s_height:
            self.rect.x = random.randrange(0, s_width)
            self.rect.y = random.randrange(-1000, 0)
        # if Game.score_value >=1000 :
        #     self.kill()
        self.shoot_enemy()
    def shoot_enemy(self):
        if self.rect.y in (0,100,250,500):
            enemybullet = EnemyBullet(enemy_bullet)
            enemybullet.rect.x = self.rect.x + 15
            enemybullet.rect.y = self.rect.y + 40
            enemybullet_group.add(enemybullet)
            sprite_group.add(enemybullet)
            pygame.mixer.Sound.set_volume(self.sound,0.5)
            self.sound.play()

class Enemy2(Enemy):

    def __init__(self, img):
        super().__init__(img)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect.x = -150
        self.rect.y = 200
        self.move = 1
        

    def update(self):
        self.rect.x += self.move
        if self.rect.x > s_width + 150:
            self.move *= -1
        elif self.rect.x <-150:
            self.move *= -1
        self.shoot_enemy2()
    def shoot_enemy2(self):
        if self.rect.x % 50 == 0 :
            enemy2bullet = EnemyBullet(enemy_bullet)
            enemy2bullet.rect.x = self.rect.x + 25
            enemy2bullet.rect.y = self.rect.y + 30
            enemy2bullet_group.add(enemy2bullet)
            sprite_group.add(enemy2bullet)


class Enemy2_1(Enemy):

    def __init__(self, img):
        super().__init__(img)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect.x = s_width + 150
        self.rect.y = 400
        self.move = -1

    def update(self):
        self.rect.x += self.move
        if self.rect.x  < - 150:
            self.move *= -1
        elif self.rect.x > s_width + 150:
            self.move *= -1
        self.shoot_enemy2_1()

    def shoot_enemy2_1(self):
        if self.rect.x % 50 == 0:
            enemy2bullet = EnemyBullet(enemy_bullet)
            enemy2bullet.rect.x = self.rect.x + 25
            enemy2bullet.rect.y = self.rect.y + 30
            enemy2bullet_group.add(enemy2bullet)
            sprite_group.add(enemy2bullet)
        
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
        self.image = pygame.transform.scale(self.image, (15, 15))

    def update(self):
        self.rect.y += 3
        if self.rect.y > s_height:
            self.kill()




class Game :
    
    score_value = 0
    # count_hit2 = 0
    def __init__(self):
        self.count_hit = 0
        self.count_hit2 = 0
        self.count_hit3 = 0
        self.level = 10
        self.lives = 3
        self.run_game()

    def create_background(self):
        for i in range(50):
            x = random.randint(1,7)
            background_image = Background(x,x)
            background_image.rect.x = random.randrange(0,s_width)
            background_image.rect.y = random.randrange(0,s_height)
            background_group.add(background_image)
            sprite_group.add(background_image)
    def bg_music(self):
        pygame.mixer.music.load(bgmusic)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)
        


    def create_player(self):
        self.player = Player(player_one)
        player_group.add(self.player)
        sprite_group.add(self.player)
    
    def create_enemy_level1(self):
        for i in range (7):
            self.enemy = Enemy(enemy_one)
            enemy_group.add(self.enemy)
            sprite_group.add(self.enemy)
    
    def create_enemy2(self):
        for i in range(1):
            self.enemy_2 = Enemy2(enemy2)
            enemy2_group.add(self.enemy_2)
            sprite_group.add(self.enemy_2)

    def create_enemy2_1(self):
        for i in range(1):
            self.enemy_2_1 = Enemy2_1(enemy2_1)
            enemy2_1group.add(self.enemy_2_1)
            sprite_group.add(self.enemy_2_1)
    
    def playerbullet_hits_enemy(self):
        hits = pygame.sprite.groupcollide(enemy_group,playerbullet_group, False, True)
        for i in hits :
            self.count_hit +=1
            if self.count_hit == 2:
                Game.score_value += 100
                i.rect.x = random.randrange(0,s_width)
                i.rect.y = random.randrange(-3000,-100)
                self.count_hit = 0

    def playerbullet_hits_enemy2(self):
        hits = pygame.sprite.groupcollide(enemy2_group,playerbullet_group, False, True)
        for i in hits:
            self.count_hit2 +=1
            if self.count_hit2 == 5:
                Game.score_value += 150
                i.rect.x = -150
                self.count_hit2 = 0
    def playerbullet_hits_enemy2_1(self):
        hits = pygame.sprite.groupcollide(enemy2_1group,playerbullet_group, False, True)
        for i in hits:
            self.count_hit3 +=1
            if self.count_hit3 == 5:
                Game.score_value += 150
                i.rect.x = s_width + 150
                self.count_hit3 = 0


    def enemybullet_hits_player(self):
        hits = pygame.sprite.spritecollide(self.player,enemybullet_group,True)
        if hits:
            self.lives -= 1
            if self.lives == 0:
                self.lives +=3
                # pygame.quit()
                # sys.exit()
    
    def enemy2bullet_hits_player(self):
        hits = pygame.sprite.spritecollide(
            self.player, enemy2bullet_group, True)
        if hits:
            self.lives -= 1
            if self.lives == 0:
                self.lives += 3

    def create_lives_player(self):
        self.lives_img = pygame.image.load(player_one)
        self.lives_img = pygame.transform.scale(self.lives_img,(30,30))
        n = 0
        for i in range(self.lives):
            screen.blit(self.lives_img,(0+n,s_height-50))
            n += 80

    def show_score(self):
        score = font.render('Score : ' + str(Game.score_value), True, ('white'))
        screen.blit(score,(50,50))

    
    def run_update(self):
        sprite_group.draw(screen)
        sprite_group.update()

    def run_game(self):
        self.create_background()
        self.create_player()
        self.bg_music()
        self.create_enemy2()
        self.create_enemy2_1()
        self.create_enemy_level1()
        while True:
            screen.fill('black')
            self.show_score()
            self.playerbullet_hits_enemy()
            self.enemybullet_hits_player()
            self.enemy2bullet_hits_player()
            self.playerbullet_hits_enemy2()
            self.playerbullet_hits_enemy2_1()
            self.create_lives_player()
            self.run_update()
            for event in pygame.event.get():
                if event.type == QUIT: 
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.player.shoot()
                        self.player.soundeffect()
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     mouse_presses = pygame.mouse.get_pressed()
                #     if mouse_presses[0]:
                #         self.player.soundeffect()
                #         self.player.shoot()
            pygame.display.update()
            clock.tick(FPS)

def main():
    game = Game()

if __name__ == '__main__':
    main()

Game.playerbullet_hits_enemy()
