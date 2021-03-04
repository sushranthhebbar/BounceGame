import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 512)
        pg.mixer.init()
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(100, 100)
        self.font = pg.font.match_font(FONT)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.img_dir = path.join(game_folder, 'img')
        self.map = Map(path.join(game_folder, 'map1.txt'))
        self.logo = pg.image.load(
            path.join(self.img_dir, "logo.png")).convert()
        self.logo.set_colorkey(WHITE)
        self.base = pg.image.load(
            path.join(self.img_dir, "base.png")).convert()
        self.base.set_colorkey(WHITE)
        self.spikebase = pg.image.load(
            path.join(self.img_dir, "spikebase.png")).convert()
        self.spikebase.set_colorkey(WHITE)
        self.snd_dir = path.join(game_folder, 'snd')
        self.jump = pg.mixer.Sound(path.join(self.snd_dir, 'jump.wav'))
        self.g = pg.mixer.Sound(path.join(self.snd_dir, 'g.wav'))
        self.v = pg.mixer.Sound(path.join(self.snd_dir, 'v.wav'))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'S':
                    self.spike = Spike(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill(BGCOLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # catch all events here
        self.player.acc = vec(0, PLAYER_GRAV)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.acc.x = -PLAYER_ACC
                    self.player.image = pg.transform.rotate(
                        self.player.image, 90)
                    # self.player.rect=self.player.image.get_rect()
                if event.key == pg.K_RIGHT:
                    self.player.acc.x = PLAYER_ACC
                    self.player.image = pg.transform.rotate(
                        self.player.image, -90)
                if event.key == pg.K_SPACE and self.player.signal != 0:
                    self.player.vel.y = -10
                    self.player.signal -= 1
                    self.jump.play()
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                    self.player.vel.x = 0
        self.player.move()

    def show_start_screen(self):
        self.screen.fill(LIGHTBLUE)
        self.screen.blit(self.logo, (444, 334))
        self.screen.blit(self.base, (0, 668))
        self.draw_text(TITLE, 82, RED, WIDTH/2, HEIGHT/4)
        pg.display.flip()
        self.waiting_for_key()

    def waiting_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    pg.quit()
                    quit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_RETURN:
                        waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def gameover_screen(self):
        pg.time.delay(500)
        self.screen.fill(LIGHTBLUE)
        self.screen.blit(self.spikebase, (0, 636))
        self.screen.blit(self.base, (0, 668))
        self.screen.blit(self.player.image, (WIDTH/2-30, 565))
        self.draw_text("GAMEOVER", 100, RED, WIDTH/2, HEIGHT/3)
        self.g.play()
        pg.display.flip()
        self.waiting_for_key()
        self.quit()

    def show_go_screen(self):
        pg.time.delay(500)
        self.v.play()
        self.screen.fill(LIGHTBLUE)
        self.draw_text("THANK YOU", 100, RED, WIDTH/2, HEIGHT/3)
        self.draw_text("Press ENTER to exit", 65, RED, WIDTH/2, HEIGHT*3/4)
        pg.display.flip()
        self.waiting_for_key()
        self.quit()


# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
