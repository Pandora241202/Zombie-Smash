from Zombie import Zombie, ZombieState
import pygame
import random
import os

def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((900, 600))

    run = True
    clock = pygame.time.Clock()
    zombies = []
    for i in range(5):
        zombies += [Zombie(30+180*i,50,ZombieState.NONE,screen)]
    for i in range(4):
        zombies += [Zombie(120+180*i,180,ZombieState.NONE,screen)]
    for i in range(5):
        zombies += [Zombie(30+180*i,310,ZombieState.NONE,screen)]
    for i in range(4):
        zombies += [Zombie(120+180*i,440,ZombieState.NONE,screen)]

    font_score = pygame.font.Font(os.path.join(os.path.dirname(os.path.realpath('Zombie.py')), 'Fonts/pixel-gaming-font/PixelGamingRegular-d9w0g.ttf'), 30)
    ouch_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.realpath('Zombie.py')), 'Sounds/ouch.ogg'))
    slam_zombie_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.realpath('Zombie.py')), 'Sounds/slam_zombie.ogg'))
    pygame.mixer.Sound.set_volume(ouch_sound, 0.7)

    score = 0
    count = 0

    while run:
        eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                pygame.mixer.Sound.play(slam_zombie_sound)
        
        screen.fill((255,255,255))
        
        if count % 10 == 0:
            chosen_hole = random.randint(0,17)
            while zombies[chosen_hole].state != ZombieState.NONE:
                chosen_hole = random.randint(0,17)
            zombies[chosen_hole].change_state(ZombieState.GO_UP) 
        
        for zombie in zombies:
            zombie.draw_hole()
            
            if zombie.state == ZombieState.GO_UP:
                zombie.go_up()
            if zombie.state == ZombieState.IS_SLAMED:
                zombie.fade()
            if zombie.state == ZombieState.NEED_SLAM:
                if zombie.is_slamed(eventlist):
                    pygame.mixer.Sound.play(ouch_sound)
                    score += 1
                    zombie.change_state(ZombieState.IS_SLAMED)
                elif zombie.need_go_down():
                    zombie.change_state(ZombieState.GO_DOWN)
            if zombie.state == ZombieState.GO_DOWN:
                zombie.go_down()       
            if zombie.state != ZombieState.NONE:
                zombie.draw()
        
        score_text = font_score.render(f'Score: {score}', True, (0,0, 0))
        screen.blit(score_text, (10, 10))
        
        count += 1
        
        pygame.display.flip()  
        
        clock.tick(8)
        
    pygame.quit()
    
if __name__ == '__main__':
    main()