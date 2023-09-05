from Zombie import Zombie, ZombieState
import pygame
import random
import os

def main():
    pygame.init()
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
    count = 0
    font_score = pygame.font.Font(os.path.join(os.path.dirname(os.path.realpath('Zombie.py')), 'pixel-gaming-font/PixelGamingRegular-d9w0g.ttf'), 30)
    score = 0
    
    while run:
        eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == pygame.QUIT:
                run = False
        
        screen.fill((255,255,255))
        
        if count % 10 == 0:
            chosen_hole = random.randint(0,17)
            if zombies[chosen_hole].state == ZombieState.NONE:
                zombies[chosen_hole].change_state(ZombieState.GO_UP) 
        
        for zombie in zombies:
            zombie.draw_hole()
            
            if zombie.state == ZombieState.GO_UP:
                zombie.go_up()
            elif zombie.state == ZombieState.IS_SLAMED:
                zombie.fade()
            elif zombie.state == ZombieState.NEED_SLAM:
                if zombie.is_slamed(eventlist):
                    score += 1
                    zombie.change_state(ZombieState.IS_SLAMED)
                if zombie.need_go_down():
                    zombie.change_state(ZombieState.GO_DOWN)
            elif zombie.state == ZombieState.GO_DOWN:
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