import math
import random
import threading
from data.bird import Bird

from data._pipes import Pipes
from data.score import Score

from data.polygon import Polygon, overlap_SAT

import sys
import os
import pygame
from pygame.math import Vector2
import time as t
from data.timer import Timer

class Button():
    def __init__(self, x, y, width, height, img):
        self.img = img
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
        # pygame.draw.rect(win, (0,0,0), (self.x-2,self.y-2,self.width+4,self.height+4), 2)

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

# rotate an image by an offset
def rotate(surface, angle, pivot:list, offset:Vector2):
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)
    rotated_offset = offset.rotate(angle)
    rect = rotated_image.get_rect(center= pivot+rotated_offset)
    return rotated_image, rect

def blit_end_numbers(screen, score_board, number_imgs):
    score = score_board.score
    numbers = tuple(int(d) for d in str(score))
    if len(numbers) == 1:
        screen.blit(number_imgs[numbers[0]], (790, 280))
    else:
        screen.blit(number_imgs[numbers[1]], (790, 280))
        screen.blit(number_imgs[numbers[0]], (745, 280))

    score = score_board.high_score
    numbers = tuple(int(d) for d in str(score))
    if len(numbers) == 1:
        screen.blit(number_imgs[numbers[0]], (790, 400))
    else:
        screen.blit(number_imgs[numbers[1]], (790, 400))
        screen.blit(number_imgs[numbers[0]], (745, 400))

def blit_number(screen, score, number_imgs, x, y):
    numbers = tuple(int(d) for d in str(score))
    if len(numbers) == 1:
        screen.blit(number_imgs[numbers[0]], (x + 45, y))
    else:
        screen.blit(number_imgs[numbers[1]], (x + 45, y))
        screen.blit(number_imgs[numbers[0]], (x, y))

def blit_medal(screen, score_board, bronze_img, silver_img, gold_img, diamond_img):
    score = score_board.score
    if score >= 40:
        screen.blit(diamond_img, (417, 290))
    elif score >= 30:
        screen.blit(gold_img, (417, 290))
    elif score >= 20:
        screen.blit(silver_img, (417, 290))
    elif score >= 10:
        screen.blit(bronze_img, (417, 290))

def play(sound, delay):
    t.sleep(delay)
    pygame.mixer.Sound.play(sound)

def app_path(path):
    bundle_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(bundle_dir, path)
    
def main():
    flags = pygame.DOUBLEBUF | pygame.HWSURFACE
    screen = pygame.display.set_mode((1280,720), vsync = 1, flags=flags)
    fullscreen = False
    
    back_img_light = pygame.image.load('data/pics/background.png').convert()
    back_img_light = pygame.transform.scale(back_img_light, (550, 1020))
    back_img_night = pygame.image.load('data/pics/nightbackground.png').convert()
    back_img_night = pygame.transform.scale(back_img_night, (550, 1020))
    back_img = back_img_light
    ground_piece_img = pygame.image.load('data/pics/ground.png').convert()
    ground_img = pygame.Surface((1336, 28))
    for i in range(47):
        ground_img.blit(ground_piece_img, (i * 28, 0))

    pipe_img_light = pygame.image.load('data/pics/pipe.png').convert_alpha()
    pipe_reversed_img_light = pygame.image.load('data/pics/pipe_reversed.png').convert_alpha()
    pipe_img_dark = pygame.image.load('data/pics/pipe_dark.png').convert_alpha()
    pipe_reversed_img_dark = pygame.image.load('data/pics/pipe_reversed_dark.png').convert_alpha()
    pipe_img = pipe_img_light
    pipe_reversed_img = pipe_reversed_img_light

    logo_img = pygame.image.load('data/pics/logo.png').convert_alpha()

    number_imgs = []
    for i in range(10):
        path = 'data/pics/numbers/' + str(i) + '.png'
        number_img = pygame.image.load(path).convert_alpha()
        number_img = pygame.transform.scale(number_img, (40, 48))
        number_imgs.append(number_img)

    start_button_img = pygame.image.load('data/pics/startbutton.png').convert()
    start_button_img = pygame.transform.scale(start_button_img, (200, 67))
    score_button_img = pygame.image.load('data/pics/scorebutton.png').convert()
    score_button_img = pygame.transform.scale(score_button_img, (200, 67))

    ok_button_img = pygame.image.load('data/pics/okbutton.png').convert()
    ok_button_img = pygame.transform.scale(ok_button_img, (200, 67))

    gameover_img = pygame.image.load('data/pics/gameover_1.png').convert_alpha()
    gameover_img = pygame.transform.scale(gameover_img, (385, 105))

    scoreboard_img = pygame.image.load('data/pics/scoreboard.png').convert_alpha()
    scoreboard_img = pygame.transform.scale(scoreboard_img, (510, 340))

    blank_scoreboard_img = pygame.image.load('data/pics/blankscoreboard.png').convert_alpha()
    blank_scoreboard_img = pygame.transform.scale(blank_scoreboard_img, (900, 600))
    best_img = pygame.image.load('data/pics/best.png').convert()
    best_img = pygame.transform.scale(best_img, (112, 51))

    bronze_img = pygame.image.load('data/pics/bronzemedal.png').convert_alpha()
    bronze_img = pygame.transform.scale(bronze_img, (160, 160))
    silver_img = pygame.image.load('data/pics/silvermedal.png').convert_alpha()
    silver_img = pygame.transform.scale(silver_img, (160, 160))
    gold_img = pygame.image.load('data/pics/goldmedal.png').convert_alpha()
    gold_img = pygame.transform.scale(gold_img, (160, 160))
    diamond_img = pygame.image.load('data/pics/diamondmedal.png').convert_alpha()
    diamond_img = pygame.transform.scale(diamond_img, (160, 160))

    orig_bird_img_1 = pygame.image.load('data/pics/Flappy Bird_1.png').convert_alpha()
    bird_img_1 = pygame.transform.scale(orig_bird_img_1, (72, 51))
    orig_bird_img_2 = pygame.image.load('data/pics/Flappy Bird_2.png').convert_alpha()
    bird_img_2 = pygame.transform.scale(orig_bird_img_2, (72, 51))
    orig_bird_img_3 = pygame.image.load('data/pics/Flappy Bird_3.png').convert_alpha()
    bird_img_3 = pygame.transform.scale(orig_bird_img_3, (72, 51))
    bird_images_light = (bird_img_3, bird_img_2, bird_img_1, bird_img_2)
    bird_img_1_dark = pygame.image.load('data/pics/Flappy Bird_1_dark.png').convert_alpha()
    bird_img_1_dark = pygame.transform.scale(bird_img_1_dark, (72, 51))
    bird_img_2_dark = pygame.image.load('data/pics/Flappy Bird_2_dark.png').convert_alpha()
    bird_img_2_dark = pygame.transform.scale(bird_img_2_dark, (72, 51))
    bird_img_3_dark = pygame.image.load('data/pics/Flappy Bird_3_dark.png').convert_alpha()
    bird_img_3_dark = pygame.transform.scale(bird_img_3_dark, (72, 51))
    bird_images_dark = (bird_img_3_dark, bird_img_2_dark, bird_img_1_dark, bird_img_2_dark)
    bird_images = bird_images_light

    start_bird_img_1 = pygame.transform.scale(orig_bird_img_1, (100, 71))
    start_bird_img_2 = pygame.transform.scale(orig_bird_img_2, (100, 71))
    start_bird_img_3 = pygame.transform.scale(orig_bird_img_3, (100, 71))
    start_bird_images = (start_bird_img_3, start_bird_img_2, start_bird_img_1, start_bird_img_2)


    flap_sound = pygame.mixer.Sound('data/music/flapping_1.mp3')
    dying_splat_sound = pygame.mixer.Sound('data/music/dying_splat.mp3')
    dying_drop_sound = pygame.mixer.Sound('data/music/dying_drop.mp3')
    score_sound = pygame.mixer.Sound('data/music/medal.mp3')

    start_button = Button(360, 500, 200, 67, start_button_img)
    score_button = Button(710, 500, 200, 67, score_button_img)
    ok_button = Button(530, 560, 200, 67, ok_button_img)
    ok_button_2 = Button(530, 610, 200, 67, ok_button_img)

    score_board = Score()

    night_filter = pygame.Surface((1280, 200))
    night_filter.set_alpha(70)
    night_filter.fill((0, 0, 0))

    death_screen = pygame.Surface((1280, 820))
    death_screen.set_alpha(255)              
    death_screen.fill((255, 255, 255))
    death_time = 0
    dead_flash = False

    ground_speed = -240 / 60
    ground_pos = -28

    start_bird = Bird(100, 71, Vector2(960, 0), Vector2(0, 0), 0)
    start_bird.flap_time = 7

    bird = Bird(72, 51, Vector2(350, 350), Vector2(0, 0), 0)
    bird.flap_time = 7
    pipes_list = []
    for i in range(5):
        xpos = 1400 + i * 300
        pipes = Pipes(100, 485, xpos, random.random() * 250 - 100)
        pipes_list.append(pipes)
    ground_points = (Vector2(0, 620), Vector2(1280, 620), Vector2(1280, 720), Vector2(0, 720))
    ground = Polygon(ground_points, Vector2(0,0), Vector2(0,0), 0)

    # font = pygame.font.SysFont('Comic Sans MS', 20)
    # font.bold = True

    # 0 = start screen, 1 = idle, 2 = playing, 3 = losing screen, 4 = scores
    stage = 0
    start_loop_frame = 0
    idle_loop_frame = 0
    lost = False
    closest_pipe = 0

    gameover_wait_time = 0
    gameover_stage = 0

    setting = 'day'

    # clock = pygame.time.Clock()
    
    clock = Timer()

    # game loop
    while True:
        dt = clock.tick(60)
        # pygame.display.set_caption(f'Running at {1/dt :.4f}.')

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if stage == 0:
                    if start_button.isOver(pos):
                        stage = 1
                    if score_button.isOver(pos):
                        stage = 4
                if stage == 4:
                    if ok_button_2.isOver(pos):
                        stage = 0
                if gameover_stage == 5:
                    if ok_button.isOver(pos):
                        score_board.reset()

                        death_screen.set_alpha(255) 
                        death_time = 0 

                        ground_pos = -28

                        start_bird = Bird(110, 78, Vector2(970, 0), Vector2(0, 0), 0)
                        start_bird.flap_time = 7

                        bird = Bird(72, 51, Vector2(350, 350), Vector2(0, 0), 0)
                        bird.flap_time = 7
                        pipes_list = []
                        for i in range(5):
                            xpos = 1400 + i * 300
                            pipes = Pipes(100, 485, xpos, random.random() * 250 - 100)
                            pipes_list.append(pipes)
                        ground = Polygon(ground_points, Vector2(0,0), Vector2(0,0), 0)

                        # 0 = start screen, 1 = idle, 2 = playing, 3 = losing screen
                        stage = 0
                        start_loop_frame = 0
                        idle_loop_frame = 0
                        lost = False
                        closest_pipe = 0

                        gameover_wait_time = 0
                        gameover_stage = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if fullscreen:
                        flags = pygame.SCALED
                        screen = pygame.display.set_mode((1280,720), flags, vsync = 1)
                        fullscreen = False
                    else:
                        flags = pygame.FULLSCREEN | pygame.SCALED
                        # screen = pygame.display.set_mode((1280,720), flags, vsync = 1)
                        screen = pygame.display.set_mode((1280,720), flags, vsync = 1)
                        fullscreen = True

                if event.key == pygame.K_m:
                    if setting == 'day':
                        bird_images = bird_images_dark
                        pipe_img = pipe_img_dark
                        pipe_reversed_img = pipe_reversed_img_dark
                        back_img = back_img_night
                        setting = 'night'

                    elif setting == 'night':
                        bird_images = bird_images_light
                        pipe_img = pipe_img_light
                        pipe_reversed_img = pipe_reversed_img_light
                        back_img = back_img_light
                        setting = 'day'

                if event.key == pygame.K_SPACE:
                    if stage == 0:
                        stage = 1
                    if gameover_stage == 5:
                        score_board.reset()

                        death_screen.set_alpha(255) 
                        death_time = 0 

                        ground_pos = -28

                        start_bird = Bird(110, 78, Vector2(970, 0), Vector2(0, 0), 0)
                        start_bird.flap_time = 7

                        bird = Bird(72, 51, Vector2(350, 350), Vector2(0, 0), 0)
                        bird.flap_time = 7
                        pipes_list = []
                        for i in range(5):
                            xpos = 1400 + i * 300
                            pipes = Pipes(100, 485, xpos, random.random() * 250 - 100)
                            pipes_list.append(pipes)
                        ground = Polygon(ground_points, Vector2(0,0), Vector2(0,0), 0)

                        # 0 = start screen, 1 = idle, 2 = playing, 3 = losing screen
                        stage = 0
                        start_loop_frame = 0
                        idle_loop_frame = 0
                        lost = False
                        closest_pipe = 0

                        gameover_wait_time = 0
                        gameover_stage = 0
                    if stage == 1:
                        stage = 2
                        bird.set_start()
                        bird.jump()
                        pygame.mixer.Sound.play(flap_sound)
                        bird.flap_time = 4
                    elif stage == 2:
                        if lost:
                            pass
                        else:
                            bird.jump()
                            pygame.mixer.Sound.play(flap_sound)

        screen.blit(back_img, (0,-400))
        screen.blit(back_img, (550,-400))
        screen.blit(back_img, (1100,-400))

        # start screen
        if stage == 0:
            d_ypos = math.cos(2 * math.pi * start_loop_frame / 60)
            screen.blit(logo_img, (320, 90 + d_ypos * 10))
            if start_loop_frame > 59:
                start_loop_frame = 0
            else:
                start_loop_frame += 1

            start_bird.pos.y = 150 + d_ypos * 10

            start_bird.update_motion()

            start_bird_img = start_bird_images[start_bird.get_img_frame()]
            start_bird_img_copy, start_bird_img_copy_rect = rotate(start_bird_img, start_bird.ang, [start_bird.pos.x, start_bird.pos.y], Vector2(0, 0))
            screen.blit(start_bird_img_copy, start_bird_img_copy_rect)

            start_button.draw(screen)
            score_button.draw(screen)

        # idle
        elif stage == 1:
            d_ypos = math.cos(2 * math.pi * idle_loop_frame / 60)
            bird.pos.y = 350 + d_ypos * 10
            if idle_loop_frame > 59:
                idle_loop_frame = 0
            else:
                idle_loop_frame += 1

            bird.update_motion()

        # start
        elif stage == 2:
            for pipes in pipes_list:
                if pipes.top_pipe.pos.x < -100:
                    del pipes_list[0]
                    pipes_list.append(Pipes(100, 485, 1400, random.random() * 250 - 100))
                    closest_pipe -= 1

            for pipes in pipes_list:
                pipes.update()

            bird.update_motion()
            bird.update()

            if pipes_list[closest_pipe].top_pipe.pos.x < bird.pos.x:
                pygame.mixer.Sound.play(score_sound)
                score_board.scored()
                closest_pipe += 1

            if lost == False:
                for i in range(closest_pipe - 1, closest_pipe + 1):
                    pipes = pipes_list[i]
                    if overlap_SAT(bird, pipes.top_pipe) or overlap_SAT(bird, pipes.bottom_pipe) or (bird.pos.y < 0 and pipes_list[closest_pipe].top_pipe.pos.x - 50 < bird.pos.x):
                        pygame.mixer.Sound.play(dying_splat_sound)
                        sound_thread = threading.Thread(target=play, args=([dying_drop_sound, 0.2]))
                        sound_thread.start()
                        dead_flash = True
                        for pipes in pipes_list:
                            pipes.top_pipe.vel = Vector2(0,0)
                            pipes.bottom_pipe.vel = Vector2(0,0)
                        score_board.end()
                        lost = True
            
                ground_pos += ground_speed
                if ground_pos <= -28:
                    ground_pos += 28
                    
            if overlap_SAT(bird, ground):
                if lost == False:
                    pygame.mixer.Sound.play(dying_splat_sound)
                    dead_flash = True
                    score_board.end()
                stage = 3
                lost = True

        elif stage == 4:
            screen.blit(blank_scoreboard_img, (190, 15))

            screen.blit(best_img, (460, 90))
            score = score_board.high_score
            blit_number(screen, score, number_imgs, 620, 90)

            screen.blit(bronze_img, (260, 160))
            score = score_board.bronze_medal
            blit_number(screen, score, number_imgs, 450, 210)
            screen.blit(silver_img, (650, 160))
            score = score_board.silver_medal
            blit_number(screen, score, number_imgs, 840, 210)
            screen.blit(gold_img, (260, 360))
            score = score_board.gold_medal
            blit_number(screen, score, number_imgs, 450, 410)
            screen.blit(diamond_img, (650, 360))
            score = score_board.diamond_medal
            blit_number(screen, score, number_imgs, 840, 410)

        if stage != 0 and stage != 4:
            for pipes in pipes_list:
                screen.blit(pipe_reversed_img, (pipes.top_pipe.points[3]))
                screen.blit(pipe_img, (pipes.bottom_pipe.points[0]))
                # pygame.draw.polygon(screen, (0,0,0), pipes.top_pipe.points, 2)
                # pygame.draw.polygon(screen, (0,0,0), pipes.bottom_pipe.points, 2)

            bird_img = bird_images[bird.get_img_frame()]
            bird_img_copy, bird_img_copy_rect = rotate(bird_img, bird.ang, [bird.pos.x, bird.pos.y], Vector2(0, 0))
            screen.blit(bird_img_copy, bird_img_copy_rect)

            # pygame.draw.polygon(screen, (0,0,0), bird.points, 2)
            # pygame.draw.polygon(screen, (0,0,0), ground.points, 2)

            if gameover_stage == 0:
                score = score_board.score
                numbers = tuple(int(d) for d in str(score))
                if len(numbers) == 1:
                    screen.blit(number_imgs[numbers[0]], (615, 30))
                else:
                    screen.blit(number_imgs[numbers[1]], (625, 30))
                    screen.blit(number_imgs[numbers[0]], (580, 30))

        # ground
        pygame.draw.rect(screen, (222, 216, 149), pygame.Rect(0, 620, 1280, 300))
        screen.blit(ground_img, (ground_pos, 620))
        if setting== 'night':
            screen.blit(night_filter, (0, 620))

        # if stage == 0:
            # notices = font.render('Press f to toggle fullscreen, m to switch modes', True, (255, 255, 255))
            # screen.blit(notices, (20, 660))

        if stage == 4:
            ok_button_2.draw(screen)

        if lost == True:
            if gameover_stage == 0:
                gameover_wait_time += 1
                if gameover_wait_time == 40:
                    gameover_stage = 1
                    gameover_wait_time = 0

            elif gameover_stage == 1:
                ti = gameover_wait_time / 20
                dy = math.sin(math.pi * ti) * 10
                y = 40 - dy
                alpha = ti * 255
                gameover_img.set_alpha(alpha)
                screen.blit(gameover_img, (440, y))

                gameover_wait_time += 1
                if gameover_wait_time == 21:
                    gameover_stage = 2
                    gameover_wait_time = 0

            elif gameover_stage == 2:
                screen.blit(gameover_img, (440, 40))

                gameover_wait_time += 1
                if gameover_wait_time == 30:
                    gameover_stage = 3
                    gameover_wait_time = 0

            elif gameover_stage == 3:
                screen.blit(gameover_img, (440, 40))

                dy = (1 - math.sin(0.5 * math.pi * gameover_wait_time / 30)) * 500
                y = 180 + dy
                screen.blit(scoreboard_img, (380, y))
            
                gameover_wait_time += 1
                if gameover_wait_time == 30:
                    gameover_stage = 4
                    gameover_wait_time = 0

            elif gameover_stage == 4:
                screen.blit(gameover_img, (440, 40))
                screen.blit(scoreboard_img, (380, 180))

                blit_end_numbers(screen, score_board, number_imgs)

                blit_medal(screen, score_board, bronze_img, silver_img, gold_img, diamond_img)

                gameover_wait_time += 1
                if gameover_wait_time == 30:
                    gameover_stage = 5
                    gameover_wait_time = 0

            elif gameover_stage == 5:
                screen.blit(gameover_img, (440, 40))
                screen.blit(scoreboard_img, (380, 180))

                blit_end_numbers(screen, score_board, number_imgs)
                
                blit_medal(screen, score_board, bronze_img, silver_img, gold_img, diamond_img)

                ok_button.draw(screen)

        if dead_flash:
            if death_time >= 255:
                dead_flash = False
            screen.blit(death_screen, (0,0))
            death_time += 12
            death_screen.set_alpha(255 - death_time)

        pygame.display.flip()

if __name__ == '__main__':
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    pygame.init()
    main()
    pygame.quit()
    sys.exit()
