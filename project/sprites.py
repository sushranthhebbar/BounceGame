import pygame as pg
from os import path
from settings import *
vec=pg.math.Vector2
coll=pg.sprite.collide_rect
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
	#self.image=pg.transform.rotate(Surface,5)
        self.image=pg.image.load(path.join(self.game.img_dir,"Bounce.png")).convert()
        self.image.set_colorkey(WHITE)
	self.pos=vec(x*TILESIZE,y*TILESIZE)
	self.vel=vec(0,0)
	self.acc=vec(0,0)
        self.rect = self.image.get_rect()
	self.rect.center=self.pos
	self.signal=2

    def move(self):
	self.vel+=self.acc
	self.collide_with_walls()
	self.collide_with_spikes()

    def collide_with_spikes(self):
	for spike in self.game.spikes:
		hits=coll(self,spike)
	        if hits:
		   self.game.gameover_screen()
    def collide_with_walls(self):
	last=self.rect.copy()
	new=self.rect
	new.x+=self.vel.x+0.5*self.acc.x
	new.y+=self.vel.y+0.5*self.acc.y
	for wall in self.game.walls:
	       if last.right<=wall.rect.left and new.right>=wall.rect.left and coll(self,wall):
		  new.right=wall.rect.left
		  self.vel.x=0
	       if last.left>=wall.rect.right and new.left<=wall.rect.right and coll(self,wall):
		  new.left=wall.rect.right
		  self.vel.x=0
               if last.top>=wall.rect.bottom and new.top<wall.rect.bottom and coll(self,wall):
		  new.top=wall.rect.bottom
		  self.vel.y=0
               if last.bottom<=wall.rect.top and new.bottom>wall.rect.top and coll(self,wall):
		  new.bottom=wall.rect.top
 		  self.signal=2
		  self.vel.y=0
	if self.rect.x<-32:
	   self.game.show_go_screen() 
class Spike(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites,game.spikes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image=pg.image.load(path.join(self.game.img_dir,"SteelspikeUp.png")).convert()
	self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image=pg.image.load(path.join(self.game.img_dir,"brick1.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
