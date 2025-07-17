import pygame
import sys
from Visual_Setup import initialize_screen, Background, Dino_Character, Obstacles, Progress_Bar, Menu, Button


def start_up(screen, background):
    menu_screen = Menu(190, 20, 400, 500, "menu.png")
    clock = pygame.time.Clock()

    # Define example button actions
    def play_action():
        print("Play button clicked!")
        nonlocal in_menu
        in_menu = False  # Exit menu and start the game

    def load_action():
        print("Options button clicked!")

    def data_action():
        print("Options button clicked!")

    def quit_action():
        print("Quit button clicked!")
        pygame.quit()
        sys.exit()

    # Create buttons (adjust x,y,width,height as you want)
    play_button = Button(
        x=245, y=100,
        width=300, height=80,
        image_idle="unpressed.png",
        image_hover="hover.png",
        image_pressed="pressed.png",
        text="Play",
        font_size=36,
        action=play_action
    )

    load_button = Button(
        x=245, y=180,
        width=300, height=80,
        image_idle="unpressed.png",
        image_hover="hover.png",
        image_pressed="pressed.png",
        text="Load",
        font_size=36,
        action=load_action
    )

    data_button = Button(
        x=245, y=260,
        width=300, height=80,
        image_idle="unpressed.png",
        image_hover="hover.png",
        image_pressed="pressed.png",
        text="Data",
        font_size=36,
        action=data_action
    )

    quit_button = Button(
        x=245, y=340,
        width=300, height=80,
        image_idle="unpressed.png",
        image_hover="hover.png",
        image_pressed="pressed.png",
        text="Quit",
        font_size=36,
        action=quit_action
    )


    buttons = [play_button, load_button, data_button, quit_button]

    in_menu = True
    while in_menu:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        background.update(0)
        background.draw(screen)

        menu_screen.draw(screen)

        # Update and draw buttons
        for button in buttons:
            button.update(events)
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def game(screen, background):

    clock = pygame.time.Clock()

    score = 0  
    font = pygame.font.SysFont(None, 36)  

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
    progress_bar = Progress_Bar(x=170, y=540, width=400, height=40, max_progress=20, bar_bg_image="progressbar.png")

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

            progress_bar.max_progress = current_obstacle.presses_required
            progress_bar.reset()

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

                    score += 1
                else:
                    current_obstacle.made_jump = False
                    game_over = True
                    challenge_active = False

        # Update dino animations and physics
        dino.animate(dino.running_frames)
        dino.update()

        # Update obstacle position only if not game over
        if not game_over:
            speed = 1 if challenge_active else 8
            background.update(speed)
        
        if not game_over:
            speed = 1 if challenge_active else 8
            current_obstacle.update(speed)

        # Regenerate obstacle if it moves off screen
        if current_obstacle.rect.right < 0:
            current_obstacle = Obstacles.randomly_generate_obstacle()
            space_press_count = 0
            challenge_active = False
            dino.resume()


        background.draw(screen)
        progress_bar.draw(screen)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))  

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




def main():

    pygame.init()
    screen = initialize_screen()
    background = Background("background.jpg")
    start_up(screen, background)
    game(screen, background)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()