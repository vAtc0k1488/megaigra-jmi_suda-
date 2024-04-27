from pygame import *
from random import  randint
from time import time as timer
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('Победа!', True, (255, 255, 255))
lose = font1.render('Проигрыш!', True, (180, 0, 0))

window = display.set_mode((700, 500))
display.set_caption("Shooter")
background = transform.scale(image.load("fon.webp"), (700, 500))
win_width = 700
win_height = 500

img_bullet = "bullet.png" 
img_enemy = "negr.png"
lost = 0
score = 0
goal = 100
max_lost = 3
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
    

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.y < win_width -  80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        

player = Player('ura.png', 300, 370,190, 75, 11)
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy('vitya.png', randint(30, win_width -30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)
bullets = sprite.Group()
for i in range(1, 6):
    monster = Enemy('negr.png', randint(80, win_width - 80), -40, 120, 80, randint(1, 5))
    monsters.add(monster)
rel_time = False
num_fire = 0
mixer.init()
mixer.music.load('diki_zapad.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
font.init()
font2 = font.SysFont('Arial', 36)
game = True 
finish = False
clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                

    if finish != True:
        window.blit(background, (0, 0))
        text = font2.render("Счёт:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        player.reset()
        player.update()
        bullets.update()                                                                   
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        monsters.update()
        asteroids.update()
        collides = sprite.groupcollide(monsters, bullets, True, True)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 120, 80, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True 
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life = life - 1
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True 
            window.blit(win, (200, 200))
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

            text_life = font1.render(str(life), 1, life_color)
            window.blit(text_life, (650, 10))
    display.update() 
    time.delay(50)
    clock.tick(FPS)

