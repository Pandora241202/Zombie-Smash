from Zombie import Zombie, ZombieState
import pygame
import random
import os
    
def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((900, 600))
    
    # UserEvent for timer
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    
    background = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath('Zombie.py')),'Images/background.png'))
    screen.blit(background, (0, 0))
        
    cursor_asset = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath('Zombie.py')), 'Images/kute_hammer.png'))
    cursor_img = pygame.transform.scale(cursor_asset, (75, 75))
    cursor_img_rect = cursor_img.get_rect()

    time = 60
    run = True
    clock = pygame.time.Clock()
    zombies = []
    for i in range(5):
        zombies += [Zombie(30+180*i,50,screen)]
    for i in range(4):
        zombies += [Zombie(120+180*i,180,screen)]
    for i in range(5):
        zombies += [Zombie(30+180*i,310,screen)]
    for i in range(4):
        zombies += [Zombie(120+180*i,440,screen)]

    font_score = pygame.font.Font(os.path.join(os.path.dirname(os.path.realpath('Zombie.py')), 'Fonts/pixel-gaming-font/PixelGamingRegular-d9w0g.ttf'), 30)
    ouch_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.realpath('Zombie.py')), 'Sounds/ouch.ogg'))
    slam_zombie_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.realpath('Zombie.py')), 'Sounds/slam_zombie.ogg'))
    pygame.mixer.Sound.set_volume(ouch_sound, 0.7)

    score = 0
    smash_time = 0
    count = 0
    
    while run:
        screen.blit(background, (0, 0)) 
        eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(slam_zombie_sound)
                smash_time += 1
            if event.type == pygame.USEREVENT: # Timer
                time -= 1
        # screen.fill((255,255,255))
        
        if time > 0:
            # Custom cursor
            pygame.mouse.set_visible(False)
            cursor_img_rect.center = pygame.mouse.get_pos()
                    
            if count % 25 == 0:
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
            
            # Text UI
            score_text = font_score.render(f'Score: {score}', True, (255,255, 255))
            screen.blit(score_text, (10, 10))
            
            smash_time_text = font_score.render(f'Smash time: {smash_time}', True, (255,255, 255))
            screen.blit(smash_time_text, (320, 10))
            
            time_text = font_score.render(f'Time left: {time}', True, (255,255, 255))
            screen.blit(time_text, (700, 10))
            
            screen.blit(cursor_img, cursor_img_rect)
            
            count += 1
            
            pygame.display.flip()  
        else:
            # Clear all zombies
            for zombie in zombies:
                zombie.reset()
            # End game
            screen.fill((132, 237, 162))
            score_text = font_score.render(f'Your score: {score}', True, (0, 0, 0))
            screen.blit(score_text, (360, 250))
            
            # Draw button
            button = pygame.Rect(350, 300, 200, 50)
            pygame.draw.rect(screen, (16, 152, 104), button)
            button_text = font_score.render('Play again', True, (255, 255, 255))
            screen.blit(button_text, (380, 310))
            
            # Enable cursor
            pygame.mouse.set_visible(True)
            
            # Click Restart button
            if button.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    time = 5
                    score = 0
                    smash_time = 0
        
            pygame.display.flip() # Update screen
            
        clock.tick(20)
        
    pygame.quit()
    
if __name__ == '__main__':
    main()
