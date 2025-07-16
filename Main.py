import pygame
import sys
from Visual_Setup import initialize_screen, Background, Dino_Character, Obstacles, Progress_Bar

pygame.init()

screen = initialize_screen()
clock = pygame.time.Clock()

background = Background("background.jpg")

dino = Dino_Character(x=0, y=200, image="frame0000.png")

t_rex_walk_frames = [
    pygame.image.load("frame0000.png").convert_alpha(),
    pygame.image.load("frame0001.png").convert_alpha(),
    pygame.image.load("frame0002.png").convert_alpha(),
    pygame.image.load("frame0003.png").convert_alpha(),
    pygame.image.load("frame0004.png").convert_alpha(),
    pygame.image.load("frame0005.png").convert_alpha(),
    pygame.image.load("frame0006.png").convert_alpha(),
    pygame.image.load("frame0007.png").convert_alpha() 
]

dino.running_frames = t_rex_walk_frames

current_obstacle = Obstacles.randomly_generate_obstacle()
space_press_count = 0
challenge_active = False
challenge_start_time = None
challenge_duration = 3000  # milliseconds (3 seconds)
game_over = False
progress_bar = Progress_Bar(x=150, y=500, width=400, height=150, max_progress=20, bar_bg_image="progressbar.png")

running = True
while running:
    screen.fill((0, 0, 0))  # clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Count space presses only during challenge
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if challenge_active:
                space_press_count += 1
                progress_bar.update_progress()

    # Start challenge when dino is close to obstacle and challenge not active
    if current_obstacle.character_detected(dino) and not challenge_active and not dino.jumping and not dino.falling:
        dino.stop()
        background.update(0)
        challenge_active = True
        challenge_start_time = pygame.time.get_ticks()
        space_press_count = 0

    # If challenge active, check timer and presses
    if challenge_active:
        elapsed = pygame.time.get_ticks() - challenge_start_time
        if elapsed >= challenge_duration:
            required = current_obstacle.presses_required
            if space_press_count >= required:
                current_obstacle.made_jump = True
                dino.jump(current_obstacle.obstacle_type)
                dino.resume()
                challenge_active = False
                space_press_count = 0
            else:
                current_obstacle.made_jump = False
                game_over = True
                challenge_active = False

    # Update dino animations and physics
    dino.animate(dino.running_frames)
    dino.update()

    # Update obstacle position only if not game over
    if not game_over:
        speed = 0 if challenge_active else 8
        background.update(speed)
    
    if not game_over:
        speed = 0 if challenge_active else 8
        current_obstacle.update(speed)

    # Regenerate obstacle if it moves off screen
    if current_obstacle.rect.right < 0:
        current_obstacle = Obstacles.randomly_generate_obstacle()
        space_press_count = 0
        challenge_active = False
        dino.resume()


    background.draw(screen)
    progress_bar.draw(screen)

    # Draw dino and obstacle
    dino.draw(screen)
    screen.blit(current_obstacle.image, current_obstacle.rect)

    # If game over, display message and stop updating
    if game_over:
        font = pygame.font.SysFont(None, 48)
        text = font.render("Game Over! Not enough presses.", True, (255, 0, 0))
        screen.blit(text, (100, 250))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
